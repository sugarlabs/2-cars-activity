#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import pygame
import sugargame
import sugargame.canvas
import pygame
from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.activity.widgets import StopButton

import game


class Activity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.max_participants = 1
        self.sound = True
        self.game = game.Game()
        self.build_toolbar()
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self,
            main=self.game.run,
            modules=[pygame.display, pygame.mixer, pygame.font])

        self.set_canvas(self._pygamecanvas)
        self._pygamecanvas.grab_focus()

    def build_toolbar(self):

        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()

        activity_button = ActivityToolbarButton(self)
        toolbar_box.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(False)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        button = ToolButton('speaker-muted-100')
        button.set_tooltip(_('Sound'))
        button.connect('clicked', self.sound_control)
        button.show()

        toolbar_box.toolbar.insert(button, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()
        stop_button.connect('clicked', self._stop_cb)

    def _stop_cb(self, button):
        self.game.running = False

    def sound_control(self, button):
        self.sound = not self.sound
        self.game.sound = self.sound
        if not self.sound:
            button.set_icon_name('speaker-muted-000')
            button.set_tooltip(_('No sound'))
        else:
            button.set_icon_name('speaker-muted-100')
            button.set_tooltip(_('Sound'))
        self.game.toggle_mute()

    def get_preview(self):
        return self._pygamecanvas.get_preview()
