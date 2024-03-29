import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gettext import gettext as _
from random import randint


# Objects are circles and squares, Elements are objects and cars
class Element(object):
    def __init__(self, game):
        self.x_to_draw = game.OBJECTS_X_POSITIONS[randint(0, 3)]
        self.y_to_draw = -10

        if (self.x_to_draw in (game.OBJECTS_X_POSITIONS[0],
                               game.OBJECTS_X_POSITIONS[1])):
            object_index = randint(0, 1)
            self.object = game.OBJECT_LIST[object_index]
        else:
            object_index = randint(2, 3)
            self.object = game.OBJECT_LIST[object_index]

    def display(self, game):
        self.object_rect = self.object.get_rect(
            center=(self.x_to_draw + self.object.get_width() // 2,
                    self.y_to_draw + self.object.get_height() // 2))
        self.car1_rect = game.leftcar.get_rect(
            center=(game.leftcar_x + game.leftcar.get_width() // 2,
                    game.car_y + game.leftcar.get_height() // 2))
        self.car2_rect = game.rightcar.get_rect(
            center=(game.rightcar_x + game.rightcar.get_width() // 2,
                    game.car_y + game.rightcar.get_height() // 2))
        # Change perceived speed of cars
        self.y_to_draw += game.background_height * 0.0065

        self.objects_interactions(game)
        game.screen.blit(self.object, (self.x_to_draw, self.y_to_draw))
        if self.y_to_draw >= game.screen_height:
            game.objectlist.remove(self)

    def objects_interactions(self, game):
        if self.object_rect.colliderect(self.car1_rect) or \
                self.object_rect.colliderect(self.car2_rect):
            if self.object in (game.red_square, game.blue_square):
                game.collision = True
                game.hit.play(0)
            if self.object in (game.red_circle, game.blue_circle):
                game.scoresound.play(0)
                game.score += 1
                game.objectlist.remove(self)

        if self.object in (game.red_circle, game.blue_circle) and (
                self.y_to_draw >= game.car_y + game.car_height):
            game.miss.play(0)
            game.coin_miss = True
