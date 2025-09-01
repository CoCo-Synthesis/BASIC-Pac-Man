# BASIC-PAC-MAN

A Pac-Man style game written in BASIC for the Tandy Color Computer 3.

Released for SEPTANDY 2025 by **CoCo-Synthesis**.

## History

I started working on this game around 1992 while in college.  I had discovered the [FontOGenic III](https://colorcomputerarchive.com/repo/Disks/Applications/Fontogenic%203%20%28Todd%20Knudsen%29%20%28Coco%203%29.zip) BASIC program that allowed you to create and save custom character sets that could be used with the BASIC HPRINT command and this had me thinking I could make a Pac Man game that used simple text screen mechanics where movement is more like the [Coleco Mini Arcade](https://itizso.itch.io/coleco-pacman) but with the benefit of higher resolution graphics by using the custom characters as "tiles." Even though I made substantial progress on the game, I never achieved a version that was playable, let alone complete.

## 33 years later...

I rescued my old Color Computer 3 from my parent's attic in May 2025, complete with almost 100 5.25" floppy diskettes that had been baking in the Texas heat for close to thirty years.  After getting [Drivewire](https://www.cocopedia.com/wiki/index.php/Getting_Started_with_DriveWire) working, I was able to rescue many of my old projects from those fragile floppies, including my incomplete Pac-Man program.

Using Visual Studio Code, I was able to restart my old work in progress.  Copilot was able to add some quick comments to the code to quickly get me up to speed on what my old code was doing.  From there, it was not just a matter of finishing the existing code, it was also a matter of optimizing it so that it was playable and not too slow.

## Optimizing BASIC

It turns out that what I thought was elegant BASIC code was horrible for running "fast."  I didn't know at the time I started the project that you could improve the speed of your program by playing to the BASIC interpretter's strengths and avoiding it's weaknesses.  Shout out to [Sub-etha Software](https://subethasoftware.com/) and the "accidental" [Optimizing Color BASIC e-book](https://colorcomputerarchive.com/repo/Documents/Books/Optimizing%20Color%20BASIC%20(Allen%20C.%20Huffman).pdf) for the informative optimization tips!

Unfortunately, this meant I needed to essentially rewrite most of the program, and do it in a way that is soooooo ugly to look at.  There's probably still room for some improved speed, but I consider it playable and I'm worried that further efficiencies require rebuilding the code from the ground up, and possibly abandoning the HPRINT commands... but that would sort of undermine the original spirit of the project. 

I also want to thank [CoCoNut Bob](https://www.youtube.com/@CoCoNutBob) for letting me know about the POKEs to alter the HPRINT command so that it clears out the background instead of leaving it transparent.  That reduced the amount of HPRINTing in the code.

## Sound Effects

The music and sound effects use the PLAY command with the Tempo (T) set to 255, and every Note Length played at 255.  Back in the early nineties, composing these PLAY commands would have been tedious and probably not very successful in mimicking the intended sound unless the programmer had severe OCD.  Luckily, I was able to use Copilot (ChatGPT 4.1) to create a Python script that can take any WAV or MP3 file and generate a set of PLAY commands that approximate the dominant note and volume level every 1/60th of a second.  It worked pretty well for generating the intro music and did very well for the remaining sound effects.

## Screenshots

### Start Screen
![Pac-Man Start Screen](Ready%20Screenshot.jpg)
