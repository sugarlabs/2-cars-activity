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
import sys

import pygame
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

FPS = 60
BLACK = (0, 0, 0)

WELCOMESCREEN_PATH = os.path.join("assets", "welcomescreen.png")
PLAY_BUTTON_PATH = os.path.join("assets", "play.png")
RULESCREEN_PATH = os.path.join("assets", "rules.png")


class Welcomescreen:
    def __init__(self, game):
        self.running = True

        self.welcomescreen = self.load_scaled_image(
            WELCOMESCREEN_PATH,
            (game.background_width,
             game.background_height))

        self.play_dimensions = (game.background_width * 0.24)
        self.play_button = self.load_scaled_image(
            PLAY_BUTTON_PATH, (self.play_dimensions, self.play_dimensions))

        self.rulescreen = self.load_scaled_image(
            RULESCREEN_PATH, (game.background_width, game.background_height))

    def load_scaled_image(self, path, size):
        width, height = size
        image = pygame.image.load(path)
        scaled_image = pygame.transform.scale(
            image.convert_alpha(), (int(width), int(height)))
        return scaled_image

    def run(self, game):
        clock = pygame.time.Clock()
        left_click_pressed = False
        ruleflag = 0  # 0 for welcome screen, 1 for rules screen

        while self.running:
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if (event.type == pygame.KEYDOWN and
                   (event.key == pygame.K_LEFT or
                       event.key == pygame.K_RIGHT)):
                    if ruleflag == 0:
                        ruleflag = 1
                    else:
                        return
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_click_pressed = True

            mos_x, mos_y = pygame.mouse.get_pos()

            game.screen.fill(BLACK)

            # Show Welcome screen
            if ruleflag == 0:
                game.screen.blit(self.welcomescreen, (game.background_x, 0))

                # Check if start button is hovered
                if self.play_button.get_rect(
                   center=((game.middle_of_screen_x),
                           (game.screen_height // 2))).collidepoint(
                               mos_x, mos_y):
                    self.play_button_rescaled = pygame.transform.scale(
                        self.play_button, (int(self.play_dimensions * 1.1),
                                           int(self.play_dimensions * 1.1)))
                    game.screen.blit(
                        self.play_button_rescaled, (
                            game.middle_of_screen_x - (
                                self.play_dimensions) * 1.1 // 2,
                            game.screen_height // 2 - (
                                self.play_dimensions) * 1.1 // 2))
                    if left_click_pressed:
                        left_click_pressed = False
                        ruleflag = 1
                else:
                    game.screen.blit(self.play_button, (
                        game.middle_of_screen_x - (self.play_dimensions) // 2,
                        game.screen_height // 2 - (self.play_dimensions) // 2))

            # Show Rules screen
            else:
                game.screen.blit(self.rulescreen, (game.background_x, 0))

                # Check if start button is hovered
                if self.play_button.get_rect(
                    center=((game.middle_of_screen_x),
                            (game.screen_height * 0.8))).collidepoint(
                                mos_x, mos_y):
                    self.play_button_rescaled = pygame.transform.scale(
                        self.play_button,
                        (int(self.play_dimensions * 1.1),
                         int(self.play_dimensions * 1.1)))
                    game.screen.blit(
                        self.play_button_rescaled, (
                            game.middle_of_screen_x - (
                                self.play_dimensions) * 1.1 // 2,
                            game.screen_height * 0.8 - (
                                self.play_dimensions) * 1.1 // 2))
                    if left_click_pressed:
                        return
                else:
                    game.screen.blit(self.play_button, (
                        game.middle_of_screen_x - (
                            self.play_dimensions) // 2,
                        game.screen_height * 0.8 - (
                            self.play_dimensions) // 2))
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()
        sys.exit()
