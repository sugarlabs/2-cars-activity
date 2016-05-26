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


import os
import gtk
import pickle
import pygame
import sys
from gettext import gettext as _


class scorescreen:

    def run(self, g, scores):

        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        clock = pygame.time.Clock()

        crashed = False

        press = 0

        land1x = 350

        scorescreen = pygame.image.load("assets/scorescreen.png").convert()
        scorescreen = pygame.transform.scale(scorescreen, (490, 768))

        restart = pygame.image.load("assets/restart.png")
        restart = pygame.transform.scale(restart, (120, 120))

        # font load

        #font_path = "fonts/sans.ttf"
        #font_size = 55
        #font1= pygame.font.Font(font_path, font_size)
        font2 = pygame.font.Font("fonts/gobold-light.ttf", 30)
        font3 = pygame.font.Font("fonts/vanadine.ttf", 80)
        # font4=pygame.font.Font("fonts/sans.ttf",20)

        # Scores load

        if os.path.getsize("score.pkl") == 0:

            with open('score.pkl', 'wb') as output:
                pickle.dump(0, output, pickle.HIGHEST_PROTOCOL)

        with open('score.pkl', 'rb') as input:  # REading
            maxscore = pickle.load(input)

        scores

        if(scores > maxscore):
            with open('score.pkl', 'wb') as output:
                pickle.dump(scores, output, pickle.HIGHEST_PROTOCOL)

            maxscore = scores

        # GAME LOOP BEGINS !!!

        while not crashed:
            # Gtk events
            while gtk.events_pending():
                gtk.main_iteration()
            for event in pygame.event.get():
                # totaltime+=timer.tick()
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    # swoosh.play(0)
                    return 1

            # print "help"
            mos_x, mos_y = pygame.mouse.get_pos()

            g.gameDisplay.fill(white)

            g.gameDisplay.blit(scorescreen, (350, 0))

            # print scores

            msg = font3.render(_("GAME OVER"), 2, white)
            g.gameDisplay.blit(msg, (450, 120))

            scoress = font2.render(_("SCORE      ") + _(str(scores)), 2, white)

            g.gameDisplay.blit(scoress, (550, 265))

            scoress = font2.render(_("BEST        ") +
                                   _(str(maxscore)), 2, white)

            g.gameDisplay.blit(scoress, (550, 330))

            if restart.get_rect(center=(550 + 60, 420 + 60)).collidepoint(mos_x, mos_y):

                g.gameDisplay.blit(pygame.transform.scale(
                    restart, (124, 124)), (550 - 2, 420 - 2))
                if(pygame.mouse.get_pressed())[0] == 1:

                    return 1

            else:
                g.gameDisplay.blit(restart, (550, 420))

            # left and right black background patches

            pygame.draw.rect(g.gameDisplay, black, (0, 0, 350, 768))

            pygame.draw.rect(g.gameDisplay, black, (840, 0, 693, 768))

            pygame.display.update()
            clock.tick(60)

            if crashed == True:                       # Game crash or Close check
                pygame.quit()
                sys.exit()

        # Just a window exception check condition

        event1 = pygame.event.get()
        if event1.type == pygame.QUIT:
            crashed = True

        if crashed == True:
            pygame.quit()
            sys.exit()
