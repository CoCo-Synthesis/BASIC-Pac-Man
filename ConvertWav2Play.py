import wave
import numpy as np
import sys
from pydub import AudioSegment
import os
import tkinter as tk
from tkinter import filedialog

USE_CENTROID = False

def generate_note_table():
    notes = []
    base_freq = 60  # O1;1 is C1 = 59 Hz for CoCo
    for octave in range(1, 6):
        for note in range(1, 13):
            freq = base_freq * (2 ** ((octave - 1) + (note - 1) / 12.0))
            notes.append((octave, note, freq))
    return notes

NOTE_TABLE = generate_note_table()

def find_closest_note(freq):
    # Clamp frequency to the supported range
    min_freq = NOTE_TABLE[0][2]
    max_freq = NOTE_TABLE[-1][2]
    freq = max(min_freq, min(max_freq, freq))
    closest = min(NOTE_TABLE, key=lambda n: abs(n[2] - freq))
    return closest[0], closest[1]  # Return octave, note

def load_audio(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".mp3":
        audio = AudioSegment.from_mp3(filename).set_channels(1)
        framerate = audio.frame_rate
        samples = np.array(audio.get_array_of_samples()).astype(np.float32)
        # Normalize to -1.0 to 1.0
        if audio.sample_width == 2:
            samples /= 32768.0
        else:
            samples = (samples - 128) / 128.0
        return samples, framerate
    else:
        with wave.open(filename, 'rb') as wf:
            framerate = wf.getframerate()
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            n_frames = wf.getnframes()
            audio = wf.readframes(n_frames)
            dtype = np.int16 if sampwidth == 2 else np.uint8
            data = np.frombuffer(audio, dtype=dtype)
            if n_channels > 1:
                data = data[::n_channels]  # Take one channel
            # Normalize data
            if sampwidth == 2:
                data = data.astype(np.float32) / 32768.0
            else:
                data = (data.astype(np.float32) - 128) / 128.0
            return data, framerate

def wav_to_play_command(filename):
    data, framerate = load_audio(filename)
    samples_per_note = int(framerate / 60)  # 1/60th second per note
    silence_threshold = 0.02  # Adjust as needed

    # First pass: find max RMS (excluding silence)
    rms_values = []
    for i in range(0, len(data), samples_per_note):
        chunk = data[i:i+samples_per_note]
        if len(chunk) < samples_per_note:
            break
        rms = np.sqrt(np.mean(chunk**2))
        if rms >= silence_threshold:
            rms_values.append(rms)
    max_rms = max(rms_values) if rms_values else 1.0  # Avoid division by zero

    # Second pass: generate PLAY command
    play_cmd = []
    prev_octave = None
    prev_note = None
    prev_volume = None

    for i in range(0, len(data), samples_per_note):
        chunk = data[i:i+samples_per_note]
        if len(chunk) < samples_per_note:
            break
        max_amp = np.max(np.abs(chunk))
        rms = np.sqrt(np.mean(chunk**2))
        if max_amp < silence_threshold or rms < silence_threshold:
            play_cmd.append("P255")
            prev_octave = None
            prev_note = None
            # Do NOT reset prev_volume here
            print(f"Window {i//samples_per_note}: Silence detected.")
            continue
        # Normalize volume to 1-31 using max RMS
        volume = int(np.clip((rms / max_rms) * 31, 1, 31))
        windowed = chunk * np.hanning(len(chunk))
        fft = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(chunk), 1/framerate)
        fft_magnitude = np.abs(fft[:len(fft)//2])
        freqs_half = freqs[:len(fft)//2]

        if USE_CENTROID:
            if np.sum(fft_magnitude) > 0:
                dom_freq = np.sum(freqs_half * fft_magnitude) / np.sum(fft_magnitude)
            else:
                dom_freq = 0
            print(f"Window {i//samples_per_note}: Centroid frequency = {dom_freq:.2f} Hz, Volume = {volume}")
        else:
            idx = np.argmax(fft_magnitude[1:]) + 1  # skip DC
            dom_freq = abs(freqs_half[idx])
            print(f"Window {i//samples_per_note}: Peak frequency = {dom_freq:.2f} Hz, Volume = {volume}")

        octave, note = find_closest_note(dom_freq)
        note_str = ""
        if volume != prev_volume:
            note_str += f"V{volume};"
            prev_volume = volume
        if octave != prev_octave:
            note_str += f"O{octave};{note}"
            prev_octave = octave
            prev_note = note
        elif note != prev_note:
            note_str += f"{note}"
            prev_note = note
        else:
            note_str += f"{note}"
        play_cmd.append(note_str)

    return play_cmd

def print_play_commands(play_cmd, max_len=240, output_file="PLAY.BAS"):
    prefix = 'PLAY "'
    suffix = '"'
    current = prefix
    line_num = 10
    lines = []
    for note in play_cmd:
        # +1 for semicolon unless it's the first note in the command
        addition = (";" if len(current) > len(prefix) else "") + note
        if len(current) + len(addition) + len(suffix) > max_len:
            lines.append(f"{line_num} {current + suffix}")
            line_num += 10
            current = prefix + note
        else:
            current += addition
    if len(current) > len(prefix):
        lines.append(f"{line_num} {current + suffix}")

    # Print to console
    for line in lines:
        print(line)
    # Save to file
    with open(output_file, "w") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    # If no argument, open file dialog
    if len(sys.argv) < 2:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        filename = filedialog.askopenfilename(
            title="Select WAV or MP3 file",
            filetypes=[("Audio files", "*.wav *.mp3"), ("All files", "*.*")]
        )
        if not filename:
            print("No file selected.")
            sys.exit(1)
    else:
        filename = sys.argv[1]
    play_cmd = wav_to_play_command(filename)
    print_play_commands(play_cmd)