#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
from sys import exit
from time import sleep
import codecs

pygame.init()
# You may need to adjust the following values
font_size=30; # or 24

# This defines the window size. I choose it larger than the display screen,
# then I move the window so that all the window decorations are out of the screen
# (just because I am afraid toggling fullscreen mode in a dual-display setup) 
screen_size = 900,700 # for our good old Acer 800x600 projo
#screen_size = 1300,900 # for a 1024x768 projo 

# Vertical offset. 0 is in the center, 1.0 moves one line up, -3.5 moves 3.5 lines down.
# To be adjusted depending on the beamer setup
vertical_offset=0

# if you want to change the font style, it is here
myfont = pygame.font.SysFont("dejavusans", font_size, 0, 0)


def toggle_fullscreen():
    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w,h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
    
    pygame.display.quit()
    pygame.display.init()
    
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) #HACK: work-around for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen


    
def main(filename):
    FPS = 10
    black = 0, 0, 0
    white = 255, 255, 255
    line_height=font_size*1.5
    screen = pygame.display.set_mode(screen_size,0,24)
    #screen = toggle_fullscreen()

    
    def parse_file():
        """returns an array of arrays of strings
        If the beginning of a line is a space, then it is the continuation of a multi-line phrase
        """
        #f=open(filename, 'r') didn't work with unicode
        f = codecs.open(filename, encoding='utf-8')
        lines=f.readlines()
        subtitles=[]
        scenes=[] # a list of indices of scenes, useful for quicly moving up and down
        current=[]
        for line in lines:
            if line[0:2] =="#S" :
                position=len(subtitles)+1
                scenes.append(position)
                #print(" found scene at ",position)
            if line[0]!='#':
                if line[0]==' ':
                    current.append(line.strip())
                else:
                    subtitles.append(current)
                    current = [line.strip()]
        subtitles.append(current)
        return subtitles, scenes


    def display(i):
        screen.fill(black)
        phrase=subtitles[i % len(subtitles)]
        y=1
        for line in phrase:
            text = myfont.render(line,True,white)
            text_rect = text.get_rect(center=(screen.get_width()/2, screen.get_height()/2 + line_height*(y-2-vertical_offset) )) 
            y+=1
            screen.blit(text, text_rect)
        pygame.display.update()

        print("*********************************************************")
        for j in range(-3,5):
          if(j==0 or j==1):
              print("======================================================")
          else:
              print("-----------------------------------------------")
          phrase=subtitles[(i+j) % len(subtitles)]
          for line in phrase:
            print(line)
          for k in range(4-len(phrase)):
            print()
        

    subtitles,scenes = parse_file()
    i=0
    done=False
    pygame.event.clear()
    while not done:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("Reloading")
                subtitles, scenes = parse_file()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_DOWN):
                i+=1
                display(i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                i-=1
                display(i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                # lookup in which scene we are
                j=0
                while  j<len(scenes) and scenes[j]<=i:
                    j+=1
                # now scenes[j]>i : move to next scene 
                if j>=len(scenes):
                    j=0
                i=scenes[j]
                display(i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                # lookup in which scene we are
                j=0
                while scenes[j]<i:
                    j+=1;
                # now scenes[j]>=i:  move to previous scene
                i=scenes[j-1]
                display(i)


if __name__ == "__main__":
    main(sys.argv[1])
