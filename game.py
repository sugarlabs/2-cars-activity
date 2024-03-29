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
from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import pygame

from elements import Element
from welcomescreen import Welcomescreen
from scorescreen import Scorescreen

FPS = 60

# Game states
WELCOME = 0
RULES = 1
PLAY = 2
PAUSE = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# SPEED of cars in the x-axis, lane change speed
ANGLE_LIMIT = 30
ANGLE_SPEED = 2

TICK_COUNTER_THRESHOLD = 40

FONT_PATH_ARIMO = os.path.join("fonts", "Arimo.ttf")

BACKGROUND_IMAGE_PATH = os.path.join("assets", "background.png")
REDCAR_IMAGE_PATH = os.path.join("assets", "redcar.png")
BLUECAR_IMAGE_PATH = os.path.join("assets", "bluecar.png")

SOUND_HIT_PATH = os.path.join("assets", "sounds", "hit.ogg")
SOUND_MISS_PATH = os.path.join("assets", "sounds", "miss.ogg")
SOUND_MUSIC_PATH = os.path.join("assets", "sounds", "music.ogg")
SOUND_SCORE_PATH = os.path.join("assets", "sounds", "score.ogg")

RED_CIRCLE_PATH = os.path.join("assets", "redcircle.png")
BLUE_CIRCLE_PATH = os.path.join("assets", "bluecircle.png")
RED_SQUARE_PATH = os.path.join("assets", "redsquare.png")
BLUE_SQUARE_PATH = os.path.join("assets", "bluesquare.png")


class Game:
    def __init__(self):
        self.state = WELCOME
        pygame.font.init()
        pygame.mixer.init()
        self.load_assets()

    def load_assets(self):
        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.leftcar_image = pygame.image.load(REDCAR_IMAGE_PATH)
        self.rightcar_image = pygame.image.load(BLUECAR_IMAGE_PATH)
        self.red_cricle_image = pygame.image.load(RED_CIRCLE_PATH)
        self.blue_circle_image = pygame.image.load(BLUE_CIRCLE_PATH)
        self.red_square_image = pygame.image.load(RED_SQUARE_PATH)
        self.blue_square_image = pygame.image.load(BLUE_SQUARE_PATH)

        self.hit = pygame.mixer.Sound(SOUND_HIT_PATH)
        self.miss = pygame.mixer.Sound(SOUND_MISS_PATH)
        self.music = pygame.mixer.Sound(SOUND_MUSIC_PATH)
        self.scoresound = pygame.mixer.Sound(SOUND_SCORE_PATH)

        self.sounds = [self.hit, self.miss, self.music, self.scoresound]
        self.volume = 1

    def toggle_mute(self):
        self.volume = 0 if self.volume == 1 else 1
        for sound in self.sounds:
            sound.set_volume(self.volume)

    def scale_images(self):
        self.background = pygame.transform.scale(
            self.background_image.convert(), (
                int(self.background_width), int(self.background_height)))
        self.leftcar = pygame.transform.scale(
            self.leftcar_image.convert_alpha(), (
                int(self.car_width), int(self.car_height)))
        self.rightcar = pygame.transform.scale(
            self.rightcar_image.convert_alpha(), (
                int(self.car_width), int(self.car_height)))

        self.red_circle = pygame.transform.scale(
            self.red_cricle_image, (self.obj_dimension, self.obj_dimension))
        self.blue_circle = pygame.transform.scale(
            self.blue_circle_image, (self.obj_dimension, self.obj_dimension))
        self.red_square = pygame.transform.scale(
            self.red_square_image, (self.obj_dimension, self.obj_dimension))
        self.blue_square = pygame.transform.scale(
            self.blue_square_image, (self.obj_dimension, self.obj_dimension))

    def initialize(self):
        self.screen_width, self.screen_height = \
            pygame.display.get_surface().get_size()
        self.middle_of_screen_x = self.screen_width // 2

        self.background_height = self.screen_height
        self.background_width = int(self.background_height * 0.65)
        self.background_x = (self.middle_of_screen_x -
                             self.background_width // 2)

        self.car_height = int(self.background_height * 0.12)
        self.car_width = int(self.background_height * 0.06)

        self.lane_1 = self.background_x + self.background_width // 8
        self.lane_2 = self.lane_1 + self.background_width // 4
        self.lane_3 = self.lane_2 + self.background_width // 4
        self.lane_4 = self.lane_3 + self.background_width // 4

        self.car_center = self.car_width // 2
        self.leftcar_x = self.lane_1 - self.car_center
        self.rightcar_x = self.lane_4 - self.car_center
        self.car_y = self.screen_height * 0.73

        self.obj_dimension = int(self.background_height * 0.05)
        obj_center = self.obj_dimension // 2
        self.OBJECTS_X_POSITIONS = [
            self.lane_1 - obj_center,
            self.lane_2 - obj_center,
            self.lane_3 - obj_center,
            self.lane_4 - obj_center]

        self.speed = self.background_width * 0.02

        self.score = 0
        self.left = True
        self.right = True
        self.is_left_pressed = self.is_right_pressed = False
        self.left_moved = False
        self.right_moved = False
        self.left_angle = self.right_angle = 0
        self.tick_counter = 0
        self.scale_images()
        self.font3 = pygame.font.Font(
            FONT_PATH_ARIMO, 55)

        self.OBJECT_LIST = [
            self.red_circle,
            self.red_square,
            self.blue_circle,
            self.blue_square]
        self.objectlist = []
        self.last = Element(self)
        self.objectlist.append(self.last)

        self.lastright = self.lastleft = 0
        self.collision = False
        self.coin_miss = False
        self.lastleft = self.lastright = Element(self)
        self.sound = True

    def draw_cars(self):
        self.screen.blit(pygame.transform.rotate(
            self.leftcar, self.left_angle), (self.leftcar_x, self.car_y))
        self.screen.blit(pygame.transform.rotate(
            self.rightcar, self.right_angle), (self.rightcar_x, self.car_y))

    def draw_objects(self):
        for object in self.objectlist:
            object.display(self)

    def draw_score(self):
        score_object = self.font3.render(_(str(self.score)), 1, (WHITE))
        score_x = self.middle_of_screen_x + self.background_width // 2.4
        score_y = self.screen_height * 0.03
        self.screen.blit(score_object, (score_x, score_y))

    def render(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (self.background_x, 0))
        self.draw_cars()
        self.draw_objects()
        self.draw_score()

    def handle_events(self):
        while Gtk.events_pending():
            Gtk.main_iteration()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not self.is_left_pressed:
                    self.left_moved = True
                    self.is_left_pressed = True
                elif event.key == pygame.K_RIGHT and not self.is_right_pressed:
                    self.right_moved = True
                    self.is_right_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.is_left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    self.is_right_pressed = False

    def update_tick_counter(self):
        self.tick_counter += 1
        if self.tick_counter > TICK_COUNTER_THRESHOLD:
            self.tick_counter = 0

    def handle_collision(self):
        if self.collision or self.coin_miss:
            screen = Scorescreen(self)
            return_code = screen.run(self, self.score)
            if return_code == 0:
                self.state = WELCOME  # Home button is pressed from scorescreen
            self.initialize()

    def create_object_list(self):
        if self.tick_counter == 10 or self.tick_counter == 35:
            self.soon_to_draw = Element(self)
            if self.last.x_to_draw < self.middle_of_screen_x:
                while True:
                    self.soon_to_draw = Element(self)
                    if (self.soon_to_draw.x_to_draw > self.middle_of_screen_x and
                       self.soon_to_draw.object != self.lastright.object):
                        break
                self.last = self.lastright = self.soon_to_draw
                self.objectlist.append(self.lastright)
            else:
                while True:
                    self.soon_to_draw = Element(self)
                    if (self.soon_to_draw.x_to_draw < self.middle_of_screen_x and
                       self.soon_to_draw.object != self.lastleft.object):
                        break
                self.last = self.lastleft = self.soon_to_draw
                self.objectlist.append(self.lastleft)

    def update_car_angles(self):
        if not self.left_moved:
            if self.left_angle > 0:
                self.left_angle -= ANGLE_SPEED
            if self.left_angle < 0:
                self.left_angle += ANGLE_SPEED
        if not self.right_moved:
            if self.right_angle > 0:
                self.right_angle -= ANGLE_SPEED
            if self.right_angle < 0:
                self.right_angle += ANGLE_SPEED

    def update_car_positions(self):
        left_car_left_bound = self.lane_1 - self.car_center
        left_car_right_bound = self.lane_2 - self.car_center
        right_car_left_bound = self.lane_3 - self.car_center
        right_car_right_bound = self.lane_4 - self.car_center
        if self.left_moved:
            if self.left:
                self.leftcar_x += self.speed
                if self.left_angle > -ANGLE_LIMIT:
                    self.left_angle -= ANGLE_SPEED

                if self.leftcar_x >= left_car_right_bound:
                    self.left_moved = False
                    self.left = not self.left
            else:
                self.leftcar_x -= self.speed
                if self.left_angle < ANGLE_LIMIT:
                    self.left_angle += ANGLE_SPEED
                if self.leftcar_x <= left_car_left_bound:
                    self.left_moved = False
                    self.left = not self.left

        if self.right_moved:
            if self.right:
                self.rightcar_x -= self.speed
                if self.right_angle < ANGLE_LIMIT:
                    self.right_angle += ANGLE_SPEED
                if self.rightcar_x <= right_car_left_bound:
                    self.right_moved = False
                    self.right = not self.right
            else:
                self.rightcar_x += self.speed
                if self.right_angle > -ANGLE_LIMIT:
                    self.right_angle -= ANGLE_SPEED
                if self.rightcar_x >= right_car_right_bound:
                    self.right_moved = False
                    self.right = not self.right

    def update_game_state(self):
        self.update_tick_counter()
        self.handle_collision()
        self.create_object_list()
        self.update_car_angles()
        self.update_car_positions()

    def run(self):
        self.initialize()
        clock = pygame.time.Clock()
        self.running = True
        self.music.play(-1)
        self.screen = pygame.display.get_surface()

        while self.running:
            self.render()
            if self.state == WELCOME:
                screen = Welcomescreen(self)
                screen.run(self)
                self.state = PLAY

            self.handle_events()
            self.update_game_state()

            pygame.display.update()
            clock.tick(FPS)
        return


if __name__ == "__main__":
    pygame.display.set_mode((1200, 900))
    game = Game()
    game.run()
