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
import pickle
import sys
from gettext import gettext as _

import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.activity.activity import get_activity_root

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCORESCREEN_PATH = os.path.join("assets", "scorescreen.png")
RESTART_IMAGE_PATH = os.path.join("assets", "restart.png")
HOME_IMAGE_PATH = os.path.join("assets", "home.png")
FONT_PATH = os.path.join("fonts", "Arimo.ttf")


class Scorescreen:
    def __init__(self, game):
        self.running = True

        self.scorescreen = self.load_scaled_image(
            SCORESCREEN_PATH, (490, 768))
        self.restart = self.load_scaled_image(
            RESTART_IMAGE_PATH, (120, 120))
        self.load_fonts(game)

        self.score_path = os.path.join(
            get_activity_root(), 'data', 'score.pkl')

    def load_fonts(self, game):
        self.font2 = pygame.font.Font(
            FONT_PATH, 30)
        self.font3 = pygame.font.Font(
            FONT_PATH, 80)

    # Load and Scale image
    def load_scaled_image(self, path, size):
        image = pygame.image.load(path)
        width, height = size
        scaled_image = pygame.transform.scale(
            image.convert_alpha(), (int(width), int(height)))
        return scaled_image

    def read_max_score(self):
        if not os.path.exists(self.score_path):
            open(self.score_path, 'w+')

        if os.path.getsize(self.score_path) == 0:
            with open(self.score_path, 'wb') as output:
                pickle.dump(0, output, pickle.HIGHEST_PROTOCOL)

        with open(self.score_path, 'rb') as input:
            max_score = pickle.load(input)

        return max_score

    def write_new_max_score(self, new_max_score):
        with open(self.score_path, 'wb') as output:
            pickle.dump(new_max_score, output, pickle.HIGHEST_PROTOCOL)

    def run(self, game, scores):
        clock = pygame.time.Clock()

        max_score = self.read_max_score()
        if scores > max_score:
            self.write_new_max_score(scores)
            max_score = scores

        while self.running:
            left_click_pressed = False
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_click_pressed = True

            mos_x, mos_y = pygame.mouse.get_pos()
            game.screen.fill(BLACK)
            game.screen.blit(self.scorescreen, (350, 0))

            msg = self.font3.render(_("GAME OVER"), 2, WHITE)
            game.screen.blit(msg, (350, 120))
            scoress = self.font2.render(_("SCORE      ") +
                                        _(str(scores)), 2, WHITE)
            game.screen.blit(scoress, (500, 265))
            scoress = self.font2.render(_("BEST        ") +
                                        _(str(max_score)), 2, WHITE)
            game.screen.blit(scoress, (510, 330))

            if self.restart.get_rect(
                    center=(550 + 60, 420 + 60)).collidepoint(mos_x, mos_y):
                game.screen.blit(pygame.transform.scale(
                    self.restart, (124, 124)), (550 - 2, 420 - 2))
                if left_click_pressed:
                    return 1
            else:
                game.screen.blit(self.restart, (550, 420))

            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()
        sys.exit()
