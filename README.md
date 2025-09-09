# BASIC-PAC-MAN (PAC-MAN.BAS)

A Pac-Man style game written in BASIC for the Tandy Color Computer 3.
Released for SEPTANDY 2025 by **CoCo-Synthesis**.

![Pac-Man Start Screen](Ready%20Screenshot.jpg)

## History

I started working on this game around 1992 while in college.  I had discovered the [FontOGenic III](https://colorcomputerarchive.com/repo/Disks/Applications/Fontogenic%203%20%28Todd%20Knudsen%29%20%28Coco%203%29.zip) BASIC program that allowed you to create and save custom character sets that could be used with the BASIC HPRINT command and this had me thinking I could make a Pac Man game that used simple text screen mechanics where movement is more like the [Coleco Mini Arcade](https://itizso.itch.io/coleco-pacman) but with the benefit of higher resolution graphics by using the custom characters as "tiles." Even though I made substantial progress on the game, I never achieved a version that was playable, let alone complete.

## 33 years later...

I rescued my old Color Computer 3 from my parent's attic in May 2025, complete with almost 100 5.25" floppy diskettes that had been baking in the Texas heat for close to thirty years.  After getting [Drivewire](https://www.cocopedia.com/wiki/index.php/Getting_Started_with_DriveWire) working, I was able to rescue many of my old projects from those fragile floppies, including my incomplete Pac-Man program.

Using Visual Studio Code, I was able to restart my old work in progress.  Copilot was able to add some quick comments to the code to quickly get me up to speed on what my old code was doing.  From there, it was not just a matter of finishing the existing code, it was also a matter of optimizing it so that it was playable and not too slow.

## Optimizing BASIC

It turns out that what I thought was elegant BASIC code was horrible for running "fast."  I didn't know at the time I started the project that you could improve the speed of your program by playing to the BASIC interpretter's strengths and avoiding it's weaknesses.  Shout out to [Sub-etha Software](https://subethasoftware.com/) and the "accidental" [Optimizing Color BASIC e-book](https://colorcomputerarchive.com/repo/Documents/Books/Optimizing%20Color%20BASIC%20(Allen%20C.%20Huffman).pdf) for the informative optimization tips!

Unfortunately, this meant I needed to essentially rewrite most of the program, and do it in a way that is soooooo ugly to look at.  There's probably still room for some improved speed, but I consider it playable and I'm worried that further efficiencies require rebuilding the code from the ground up, and possibly abandoning the HPRINT commands... but that would sort of undermine the original spirit of the project. 

I also want to thank [CoCoNut Bob](https://www.youtube.com/@CoCoNutBob) for letting me know about the POKEs to alter the HPRINT command so that it clears out the background instead of leaving it transparent.  That reduced the amount of HPRINTing in the code.

## Recreating Sound Effects

The music and sound effects use the PLAY command with the Tempo (T) set to 255, and every Note Length (L) set to 255.  Back in the early nineties, composing these PLAY commands would have been tedious and probably not very successful at mimicking the intended sounds unless the programmer had severe OCD.  Luckily, I was able to use Copilot (ChatGPT 4.1) to create a [Python script](ConvertWav2Play.py) that can take any WAV or MP3 file and generate a set of PLAY commands that approximate the dominant note and volume level every 1/60th of a second.  It worked pretty well for generating the intro music and did very well for the remaining sound effects.

## Game Features

### Multiple Mazes
The game includes 6 Maze Designs inspired by various versions of Pac Man.  Each Maze is contained in a data file named "MAZE {#}/DAT".  As each Maze is cleared during game play, the next sequential Maze file is loaded.  After the last Maze is loaded, the cycle starts over.  It is possible to add more custom Maze files without modifying the code as long as the data format is correct, and the filename convention is followed with the Maze number being a sequential value.  I am considering a future Maze Designer program that will make it easy to change/add Mazes.

### Multiple Bonus "Fruits"
The game has 7 of the bounus "fruits" that are part of the original Pac-Man experience.  The "Galaxian Spaceship" is the only bonus fruit missing.  Once the user clears the 7th Bounus (Bell), subsequent levels will repeat the Bell bonus fruit.

### Extra Pac-Man
The game rewards you with an extra Pac-Man every 10,000 points.

# MAZE MANAGER (MAZE MGR.BAS)

Now you can edit existing Mazes or create new ones!  The Maze Manager let's you LOAD existing mazes, create a NEW maze, and SAVE your changes.

![Maze Manager Interface](Maze%20Manager%20Interface.jpg)

## Keyboard Navigation
- Use the ARROW keys to navigate selection choices.
- Press the ENTER key to make a selection.
- Use the BREAK key to go back to the previous selection section/menu.
## Actions
The first selection section allows the user to pick from the 3 main actions:
### NEW
This action creates an "empty" maze that the user can start to build out.
### LOAD
This action displays a list of maze "levels" that the user can load for editing by selecting the desired maze. Empty mazes are displayed as grey text and selecting an empty maze level will load an "empty" maze that you can start to build out.
### SAVE
This action allows you to select a maze "level" to save commit your new or updated maze.  You will be warned if you are replacing existing Maze data.  "Empty" maze slots are displayed in grey text.
## Maze Editing
Once a maze is loaded and displayed, you can use the arrow keys to navigate which tile you want to change.
### Change Tiles
Pressing the ENTER key will allow the user to select a desired replacement tile.  Use the arrow keys to select the tile and press ENTER to update the maze.
### Change Maze Color
The Tile Selection section also has section labeled "CLR" that when selected allows you to change the maze color by selecting the UP/DOWN arrow keys.
## Maze Restrictions
### Power Pellets
- The Maze Manager requires 4 Power Pellets exist on the Maze in order for the SAVE action to be available.
- If you have 4 Power Pellets on your maze, you must remove one before you can add another one.
### Ghost Jail
Even though you can navigate over the "Ghost Jail" tiles, you cannot select them for editing.
### Pac Man Start Position
Even though you can navigate over the Pac Man at the start position, you cannot select it for editing.
### Tunnels
A tunnel can be created by not having a border tile on both the left and right side of the maze on the same grid row.  You can have as many tunnels as you want and they should function as expected.  However, the game will not yet support tunnels that run top to bottom of the maze.  Maze manager does not restrict you from creating and saving mazes with "bad" tunnels.


