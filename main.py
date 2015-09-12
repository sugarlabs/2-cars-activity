#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 2 Cars
# Copyright (C) 2015  Utkarsh Tiwari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Utkarsh Tiwari    iamutkarshtiwari@gmail.com



import gtk
import pygame
import sys



class game:
    
    
    def __init__(self):
        pass
        
    def initialize(self):

        
        
        
        self.left=True
        self.right=True
        
        self.leftclick=self.rightclick=0
        
        self.leftmove=0
        self.rightmove=0
        
        
        
        
        self.leftcar_x=390
        #510
        
        
        self.rightcar_x=760
        #600
        
        self.speed=8
        
        
        
        
        
        #self.welcomeflag=1
        #self.musicflag=False
        
        #self.left_transit=self.right_transit=0
        
        
        
        
        
        
        
        
        
        
        
        

        pygame.init()
        self.sound=True
        
        try:
            pygame.mixer.init()
        except Exception, err:
            self.sound=False
            print 'error with sound', err

        self.info=pygame.display.Info()
        
        self.gameDisplay=pygame.display.get_surface()
        
        if not(self.gameDisplay):
            
            self.gameDisplay = pygame.display.set_mode((self.info.current_w,self.info.current_h))

            pygame.display.set_caption("Flappy Birds")
            #gameicon=pygame.image.load('images/icon.png')
            #pygame.display.set_icon(gameicon)

        #self.hit=pygame.mixer.Sound("assets/sounds/hit.ogg")
        
        
        
        self.font_path = "fonts/sans.ttf"
        self.font_size = 55
        self.font1= pygame.font.Font(self.font_path,self.font_size)
        self.font2=pygame.font.Font("fonts/sans.ttf",30)
        self.font3=pygame.font.Font("fonts/sans.ttf",40)
        self.font4=pygame.font.Font("fonts/sans.ttf",23)
        
        
        
        

        # Load the images for elements
        #load_elements_images()
        
        self.background = pygame.transform.scale(pygame.image.load("assets/background.png").convert(),\
                                                 (491,768))
        
        self.leftcar = pygame.transform.scale(pygame.image.load("assets/bluecar.png"),\
                                              (45,90))
        
        
        self.rightcar = pygame.transform.scale(pygame.image.load("assets/redcar.png"),\
                                              (45,90))
        
        
      
        

    def make(self):

        self.initialize()
        
        # Variable Initialization
        black=(0,0,0)
        white=(255,255,255)
        clock=pygame.time.Clock()
            
        crashed=False   

        
        
        # GAME LOOP BEGINS !!!
        
        while not crashed:
            #Gtk events
            
            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                #totaltime+=timer.tick()
                if event.type == pygame.QUIT:
                    crashed=True
                
            mos_x,mos_y=pygame.mouse.get_pos() 
            
            
            '''
            if self.welcomeflag == 1:
                a = welcomescreen(self.gameDisplay)
                a.run()
                self.welcomeflag=0
                self.keyinit=1
                #self.dispinit()
            '''    
            
            
            self.gameDisplay.fill(white)
            self.gameDisplay.blit(self.background,(350,0))
            
            
            
            # Car Blitting
            
            self.gameDisplay.blit(self.leftcar,(self.leftcar_x,550))
            
            self.gameDisplay.blit(self.rightcar,(self.rightcar_x,550))
            
            
            #self.gameDisplay.blit(self.leftcar,(510,550))
            
            #self.gameDisplay.blit(self.rightcar,(600,550))
            
            
            
            #390
            #510
        
        
            #760
            #600
            
            
            if(self.leftmove==1):
                
                
                #For left car updation
                if(self.left==True):
                    
                    self.leftcar_x+=self.speed
                    
                    if(self.leftcar_x>=510):
                        
                        self.leftmove=0
                        self.left=not self.left
                        
                else:
                    self.leftcar_x-=self.speed
                    
                    if(self.leftcar_x<=390):
                        
                        self.leftmove=0
                        self.left=not self.left
                        
                        
            if(self.rightmove==1):            
                
                #For right car updation
                if(self.right==True):
                    
                    self.rightcar_x-=self.speed
                    
                    if(self.rightcar_x<=640):
                        
                        self.rightmove=0
                        self.right= not self.right
                        
                    
                else:
                    
                    self.rightcar_x+=self.speed
                    
                    if(self.rightcar_x>=760):
                        
                        self.rightmove=0
                        self.right=not self.right
                        
                        
                        
                        
                
                
                
            
            
            
            
            # Keyboard Input
            
            #event = pygame.event.poll()
            
            if event.type==pygame.KEYDOWN and event.key==276 and self.leftclick==0:
                #jump.play(0)
                #self.left_transit=1
                self.leftmove=1
                self.leftclick=1
                
                #self.left=not self.left
            
            #left starts moving
            
            
            
            if event.type==pygame.KEYUP and event.key==276:
                self.leftclick=0
                
                
                    
            #event = pygame.event.poll()    
            
            if event.type==pygame.KEYDOWN and event.key==275 and self.rightclick==0:
                #jump.play(0)
                self.rightmove=1
                self.rightclick=1
                
                
            #right start moving
            
            
            
            if event.type==pygame.KEYUP and event.key==275:
                self.rightclick=0
            
            
            
            
            
            
          
            
            # BLACK RECTANGLES DISPLAY
                      
            pygame.draw.line(self.gameDisplay,black,(350,0),(350,768), 1)          
            pygame.draw.line(self.gameDisplay,black,(840,0),(840,768), 1)           
                      
            pygame.draw.rect(self.gameDisplay,black,(0,0,350,768))    
                    
            pygame.draw.rect(self.gameDisplay,black,(840,0,693,768))
            
            
            
            
            
            
            pygame.display.update()
            clock.tick(60)
     
            if crashed:                                   # Game crash or Close check
                pygame.quit()
                sys.exit()
       
        # Just a window exception check condition

        event1=pygame.event.get()                                 
        if event1.type == pygame.QUIT:
            crashed=True
   
        if crashed:
            pygame.quit()
            sys.exit()
            

if __name__ == "__main__":
    g = game()
    g.make()         

            
