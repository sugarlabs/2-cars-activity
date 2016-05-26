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
from gettext import gettext as _

from elements import *
from welcomescreen import *
from scorescreen import *


class game:

    def __init__(self):
        self.start = 1

    def initialize(self):

        self.score = 0
        self.left = True
        self.right = True

        self.leftclick = self.rightclick = 0

        self.leftmove = 0
        self.rightmove = 0
        self.move = 1

        self.left_angle = self.right_angle = 0

        self.leftcar_x = 390
        # 510

        self.rightcar_x = 760
        # 600

        self.speed = 10

        self.anglespeed = 3
        self.anglelimit = 30

        # self.welcomeflag=1
        # self.musicflag=False

        # self.left_transit=self.right_transit=0

        self.objectlist = []

        self.i = 0
        self.last = element()

        self.objectlist.append(self.last)

        self.lastright = self.lastleft = 0
        self.timer = 0

        self.collision = 0

        self.lastleft = self.lastright = element()
        # self.start=1

        pygame.init()
        self.sound = True

        try:
            pygame.mixer.init()
        except Exception, err:
            self.sound = False
            print 'error with sound', err

        self.info = pygame.display.Info()

        self.gameDisplay = pygame.display.get_surface()

        if not(self.gameDisplay):

            self.gameDisplay = pygame.display.set_mode(
                (self.info.current_w, self.info.current_h))

            pygame.display.set_caption(_("2 Cars"))
            # gameicon=pygame.image.load('images/icon.png')
            # pygame.display.set_icon(gameicon)

        # self.hit=pygame.mixer.Sound("assets/sounds/hit.ogg")

        self.font_path = "fonts/sans.ttf"
        self.font_size = 55
        self.font1 = pygame.font.Font(self.font_path, self.font_size)
        self.font2 = pygame.font.Font("fonts/sans.ttf", 30)
        self.font3 = pygame.font.Font("fonts/gobold-light.ttf", 40)
        self.font4 = pygame.font.Font("fonts/sans.ttf", 23)

        # Load the images for elements
        # load_elements_images()

        self.background = pygame.transform.scale(pygame.image.load("assets/background.png").convert(),
                                                 (491, 768))

        self.leftcar = pygame.transform.scale(pygame.image.load("assets/redcar.png"),
                                              (45, 90))

        self.rightcar = pygame.transform.scale(pygame.image.load("assets/bluecar.png"),
                                               (45, 90))

        # Music load

        self.hit = pygame.mixer.Sound("assets/sounds/hit.ogg")
        self.miss = pygame.mixer.Sound("assets/sounds/miss.ogg")
        self.music = pygame.mixer.Sound("assets/sounds/music.ogg")
        self.scoresound = pygame.mixer.Sound("assets/sounds/score.ogg")

    def make(self):

        self.initialize()

        # Variable Initialization
        black = (0, 0, 0)
        white = (255, 255, 255)
        clock = pygame.time.Clock()

        crashed = False
        self.music.play(-1)

        # GAME LOOP BEGINS !!!

        while not crashed:
            # Gtk events

            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                # totaltime+=timer.tick()
                if event.type == pygame.QUIT:
                    crashed = True

            mos_x, mos_y = pygame.mouse.get_pos()

            if self.start == 1:
                a = welcomescreen()
                a.run(self)
                self.start = 0

            self.gameDisplay.fill(white)
            self.gameDisplay.blit(self.background, (350, 0))

            # Car Blitting

            self.gameDisplay.blit(pygame.transform.rotate(
                self.leftcar, self.left_angle), (self.leftcar_x, 550))

            self.gameDisplay.blit(pygame.transform.rotate(
                self.rightcar, self.right_angle), (self.rightcar_x, 550))

            # Obstacles placement

            self.i += 1

            if(self.i > 40):
                self.i = 0

            if((self.i == 10 or self.i == 35) and self.move == 1):

                self.current = element()

                check = True

                if(self.last.x < 530):

                    while(True):

                        self.current = element()
                        if(self.current.x > 530 and self.current.element != self.lastright.element):

                            break

                    self.last = self.lastright = self.current
                    self.objectlist.append(self.lastright)

                else:

                    while(True):

                        self.current = element()
                        if(self.current.x < 530 and self.current.element != self.lastleft.element):

                            break

                    self.last = self.lastleft = self.current
                    self.objectlist.append(self.lastleft)

            # Elements display

            for j in self.objectlist:

                j.display(self)

            # Score blitting

            head3 = self.font3.render(_(str(self.score)), 1, (white))
            self.gameDisplay.blit(head3, (780, 20))

            if(self.move == 0):
                self.timer += 1

                if(self.timer >= 125):
                    self.collision = 1

            if(self.collision == 1):
                a = scorescreen()
                a.run(self, self.score)
                self.initialize()

            # Car angle reorientation

            if(self.leftmove == 0):

                if(self.left_angle > 0):
                    self.left_angle -= self.anglespeed

                if(self.left_angle < 0):
                    self.left_angle += self.anglespeed

            if(self.rightmove == 0):

                if(self.right_angle > 0):
                    self.right_angle -= self.anglespeed

                if(self.right_angle < 0):
                    self.right_angle += self.anglespeed

            # Car Movements

            if(self.leftmove == 1):

                # For left car updation
                if(self.left == True):

                    self.leftcar_x += self.speed

                    # Angle update
                    if(self.left_angle > -self.anglelimit):
                        self.left_angle -= self.anglespeed

                    if(self.leftcar_x >= 510):

                        self.leftmove = 0
                        self.left = not self.left

                else:
                    self.leftcar_x -= self.speed

                    # Angle update

                    if(self.left_angle < self.anglelimit):
                        self.left_angle += self.anglespeed

                    if(self.leftcar_x <= 390):

                        self.leftmove = 0
                        self.left = not self.left

            if(self.rightmove == 1):

                # For right car updation
                if(self.right == True):

                    self.rightcar_x -= self.speed

                    # Angle update

                    if(self.right_angle < self.anglelimit):
                        self.right_angle += self.anglespeed

                    if(self.rightcar_x <= 640):

                        self.rightmove = 0
                        self.right = not self.right

                else:

                    self.rightcar_x += self.speed

                    # Angle update

                    if(self.right_angle > -self.anglelimit):
                        self.right_angle -= self.anglespeed

                    if(self.rightcar_x >= 760):

                        self.rightmove = 0
                        self.right = not self.right

            # Keyboard Input

            #event = pygame.event.poll()

            if event.type == pygame.KEYDOWN and event.key == 276 and self.leftclick == 0 and self.move == 1:
                # jump.play(0)
                # self.left_transit=1
                self.leftmove = 1
                self.leftclick = 1

                #self.left=not self.left

            # left starts moving

            if event.type == pygame.KEYUP and event.key == 276:
                self.leftclick = 0

            #event = pygame.event.poll()

            if event.type == pygame.KEYDOWN and event.key == 275 and self.rightclick == 0 and self.move == 1:
                # jump.play(0)
                self.rightmove = 1
                self.rightclick = 1

            # right start moving

            if event.type == pygame.KEYUP and event.key == 275:
                self.rightclick = 0

            # BLACK RECTANGLES DISPLAY

            pygame.draw.line(self.gameDisplay, black, (350, 0), (350, 768), 1)
            pygame.draw.line(self.gameDisplay, black, (840, 0), (840, 768), 1)

            pygame.draw.rect(self.gameDisplay, black, (0, 0, 350, 768))

            pygame.draw.rect(self.gameDisplay, black, (840, 0, 693, 768))

            pygame.display.update()
            clock.tick(60)

            # Game crash or Close check
            if crashed:
                pygame.quit()
                sys.exit()

        # Just a window exception check condition

        event1 = pygame.event.get()
        if event1.type == pygame.QUIT:
            crashed = True

        if crashed:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    g = game()
    g.make()
