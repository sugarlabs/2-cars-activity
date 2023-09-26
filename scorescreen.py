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
        self.button_size = (game.background_width * 0.24)

        self.scorescreen = self.load_scaled_image(
            SCORESCREEN_PATH, (game.background_width, game.background_height))
        self.restart = self.load_scaled_image(
            RESTART_IMAGE_PATH, (self.button_size, self.button_size))

        self.load_fonts(game)

        self.score_path = os.path.join(
            get_activity_root(), 'data', 'score.pkl')

    def load_fonts(self, game):
        self.font2 = pygame.font.Font(
            FONT_PATH, int(game.background_width * 0.06))
        self.font3 = pygame.font.Font(
            FONT_PATH, int(game.background_width * 0.16))

    def load_scaled_image(self, path, size):
        image = pygame.image.load(path)
        width, height = size
        scaled_image = pygame.transform.scale(
            image.convert_alpha(), (int(width), int(height)))
        return scaled_image

    def read_max_score(self):
        if os.path.exists(self.score_path) and \
                os.path.getsize(self.score_path) > 0:
            with open(self.score_path, 'rb') as input_file:
                max_score = pickle.load(input_file)
                return max_score
        else:
            self.write_new_max_score(0)
            return 0

    def write_new_max_score(self, new_max_score):
        with open(self.score_path, 'wb') as output_file:
            pickle.dump(new_max_score, output_file, pickle.HIGHEST_PROTOCOL)

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
            game.screen.blit(self.scorescreen, (game.background_x, 0))

            # Display GAME OVER in the middle of screen
            self.display_in_center(
                _("GAME OVER"), game.screen_height * 0.03, self.font3, game)
            # Display scores in the middle of screen
            self.display_in_center(
                _("SCORE      ") + _(str(scores)),
                game.screen_height * 0.18,
                self.font2,
                game)
            self.display_in_center(
                _("BEST         ") + _(str(max_score)),
                game.screen_height * 0.23,
                self.font2,
                game)

            restart_x = game.middle_of_screen_x

            # Check if restart button is hovered
            restart_rect = self.restart.get_rect(
                center=(restart_x, (game.screen_height // 2)))
            if restart_rect.collidepoint(mos_x, mos_y):

                self.restart_rescaled = pygame.transform.scale(
                    self.restart,
                    (int(self.button_size * 1.1),
                     int(self.button_size * 1.1)))
                game.screen.blit(
                    self.restart_rescaled,
                    (restart_x - self.button_size * 1.1 // 2,
                     game.screen_height // 2 - self.button_size * 1.1 // 2))

                if left_click_pressed:
                    return 1
            else:
                game.screen.blit(
                    self.restart,
                    (restart_x - self.button_size // 2,
                     game.screen_height // 2 - self.button_size // 2))

            pygame.display.update()
            clock.tick(FPS)

    def display_in_center(self, text, y, font, game):
        msg = font.render(text, 2, WHITE)
        text_width, text_height = msg.get_size()
        text_x = game.screen_width // 2 - text_width // 2
        game.screen.blit(msg, (text_x, y))
