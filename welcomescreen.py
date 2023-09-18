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
            WELCOMESCREEN_PATH, (490, 768))

        self.play_button = self.load_scaled_image(
            PLAY_BUTTON_PATH, (120, 120))
        self.rulescreen = self.load_scaled_image(
            RULESCREEN_PATH, (490, 768))

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or \
                            event.key == pygame.K_RIGHT:
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
                game.screen.blit(self.welcomescreen, (350, 0))
                if self.play_button.get_rect(
                        center=(530 + 60, 300 + 60)).collidepoint(
                            mos_x, mos_y):
                    game.screen.blit(pygame.transform.scale(
                        self.play_button, (124, 124)), (530 - 2, 300 - 2))
                    if left_click_pressed:
                        left_click_pressed = False
                        ruleflag = 1
                else:
                    game.screen.blit(self.play_button, (530, 300))

            # Show Rules screen
            else:
                game.screen.blit(self.rulescreen, (350, 0))
                if self.play_button.get_rect(
                        center=(530 + 60, 550 + 60)).collidepoint(
                            mos_x, mos_y):
                    game.screen.blit(pygame.transform.scale(
                        self.play_button, (124, 124)), (530 - 2, 550 - 2))
                    if left_click_pressed:
                        return
                else:
                    game.screen.blit(self.play_button, (530, 550))

            pygame.display.update()
            clock.tick(FPS)
