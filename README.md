# theater-subtitles

This program offers an easy interface for playing subtitles in a real-time theater environment.

It opens a window with the actual subtitles (to be displayed to the public somehow, on a big screen or a beamer). Meanwhile it displays in the terminal the few previous and next screens (useful when the actors skip a line... yes they sometimes do). You move from line to line using the keyboard arrows.

Simple, no frill, tried and tested: this program has been used since 2017 in a dozen representations of the Russian theater school Okno in Lyon (http://club.lycorn.free.fr/spectacles.html).


## Usage

### Usage during a representation

	 python subtitles.py MyPlayFile.txt

Use down arrow or space bar to advance to next screen, up arrow to come back to previous screen. 

The public screen always starts blank.

Use 's' and 'z' keys to jump to the beginning of next and previous scene espectively. This is mostly useful during rehearsals.

### Syntax of the text file 
The text to be displayed is read from a plain text file (UTF-8), with a trivial syntax (look at the examples above):

- any line beginning with a hash sign is a comment (not displayed) -- this is useful e.g. for character names
- a group of (at most 4) lines to be displayed together begins with an unindented line, possibly followed by indented lines, i.e. lines beginning with a space (if it is not clear, just see the example files).
The advantage is that it is very quick to edit during rehearsals, as the actors act...
- an empty line shows a blank screen to the public
- a comment line beginning with '#S' marks the beginning of a scene (for quick navigation using 's' and 'z' keys)


### Examples

A minimal commented example:

		python subtitles.py calibration.txt 

A classical play:

		python subtitles.py Plays/2021-Gozzi-Voron/Acte1.txt 

A display of poetry (translated from Russian to French):

		python subtitles.py Plays/2019-zolotoi-viek.txt


## How to prepare your subtitle file

- Acquire somehow a text version of your play.
- Do some global replace, e.g. to comment out the character names, etc. 
- Split long lines so that they fit the screen.
- During the late rehersals 
  - group lines into screens (max 4 lines per screen) according to the staging.
  - insert blanks (empty lines) where needed
  - typing 'r' reloads the subtitle file, so you may edit it while displaying it. 

The end of MyPlayFile.txt is wrapped to the beginning, and the other way round.
This is useful when preparing files (you may go directly to the end using the up arrow) but dangerous on the day of the representation: better add a few blank lines at the end of your file!


## Configuration (or the lack of it)

There is a limit of at most 4 lines of text in each screen. 
So far, this is hardcoded in subtitle.py.

No font size, window size or style option, but of course setting these up this will be necessary since each theater is different.
Currently you have to modify these features directly in the code, look for the comments...

I usually open a window that is slightly larger than the resolution of the screen/beamer, then move it using the mouse so that its borders are out of the display.

## Ack ack
The initial version of this program was written by Yulik Daniel.
