#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
from sys import exit
from time import sleep
import codecs


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

    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??

    pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
    return screen


    
def main(filename):
    FPS = 10
    pygame.init()
    black = 0, 0, 0
    white = 255, 255, 255
    font_size=30; # 24 normal
    line_height=font_size*1.5
    myfont = pygame.font.SysFont("dejavusans", font_size, 0, 0)
    screen_size = 1300,900 # for a 1024x768 proj
    #screen_size = 900,700 # forour cheap Acer 800x600 proj
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
        current=[]
        for line in lines:
            if line[0]!='#':
                if line[0]==' ':
                    current.append(line.strip())
                else:
                    subtitles.append(current)
                    current = [line.strip()]
        subtitles.append(current)
        return subtitles


    def affiche(i):
        screen.fill(black)
        phrase=subtitles[i]
        y=1
        for line in phrase:
            text = myfont.render(line,True,white)
            #text_rect = text.get_rect(center=(screen.get_width()/2,line_height*(y+1) )) # trois quarts haut
            #text_rect = text.get_rect(center=(screen.get_width()/2,line_height*(y+0.5) )) # en haut 
            text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2+line_height*(y+1) )) # en bas
            #text_rect = text.get_rect(center=(screen.get_width()/2,screen.get_height()/2.2+line_height*(y+1) )) # Au milieu
            y+=1
            screen.blit(text, text_rect)
        pygame.display.update()

        print("*********************************************************")
        for j in range(-4,6):
          if(j==0 or j==1):
              print("======================================================")
          else:
              print("--------------------------------------------------")
          phrase=subtitles[i+j]
          for line in phrase:
            print(line)
          for k in range(4-len(phrase)):
            print()
        

    subtitles = parse_file()
    i=0
    done=False
    pygame.event.clear()
    while not done:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("Reloading")
                subtitles = parse_file()

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_DOWN):
                i+=1
                affiche(i)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                i-=1
                affiche(i)


if __name__ == "__main__":
    main(sys.argv[1])
