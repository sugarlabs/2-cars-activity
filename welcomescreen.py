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


class welcomescreen:

    def __init__(self):
        pass

    def run(self, g):

        #self.gameDisplay = display

        black = (0, 0, 0)
        white = (255, 255, 255)
        clock = pygame.time.Clock()

        crashed = False

        # image load

        land = pygame.image.load("assets/welcomescreen.png").convert()
        background = pygame.transform.scale(land, (490, 768))

        play = pygame.image.load("assets/play.png")
        play = pygame.transform.scale(play, (120, 120))

        rules = pygame.image.load("assets/rules.png").convert()
        rules = pygame.transform.scale(rules, (490, 768))

        button = pygame.image.load("assets/button.png")

        font2 = pygame.font.Font("fonts/sans.ttf", 25)

        flag = 1
        ruleflag = 0

        # GAME LOOP BEGINS !!!

        while not crashed:
            # Gtk events

            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                # totaltime+=timer.tick()
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN and (event.key == 276 or event.key == 275):
                    return

            # print "help"
            mos_x, mos_y = pygame.mouse.get_pos()

            g.gameDisplay.fill(white)

            if(ruleflag == 0):

                g.gameDisplay.blit(background, (350, 0))

                if play.get_rect(center=(530 + 60, 300 + 60)).collidepoint(mos_x, mos_y):

                    g.gameDisplay.blit(pygame.transform.scale(
                        play, (124, 124)), (530 - 2, 300 - 2))
                    if(pygame.mouse.get_pressed())[0] == 1:

                        ruleflag = 1

                else:
                    g.gameDisplay.blit(play, (530, 300))

            else:

                g.gameDisplay.blit(rules, (350, 0))
                g.gameDisplay.blit(button, (540, 400))

                if play.get_rect(center=(530 + 60, 550 + 60)).collidepoint(mos_x, mos_y):

                    g.gameDisplay.blit(pygame.transform.scale(
                        play, (124, 124)), (530 - 2, 550 - 2))
                    if(pygame.mouse.get_pressed())[0] == 1:

                        return

                else:
                    g.gameDisplay.blit(play, (530, 550))

            # left and right black background patches

            pygame.draw.rect(g.gameDisplay, black, (0, 0, 350, 768))

            pygame.draw.rect(g.gameDisplay, black, (840, 0, 693, 768))

            pygame.display.update()
            clock.tick(60)

            if crashed:                        # Game crash or Close check
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
    g = welcomescreen()
    g.run(gameDisplay)
