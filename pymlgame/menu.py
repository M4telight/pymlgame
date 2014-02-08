# -*- coding: utf-8 -*-

"""
pymlgame - Menu
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

from PIL import Image

import pymlgame


class Menu(object):
    """
    A simple menu with text entries. Each entry has a callback method so it
    could be a submenu or something completely different.
    """
    def __init__(self, width=40, height=40, color=pymlgame.WHITE,
                 active=pymlgame.CYAN, bg=pymlgame.BLACK):
        """
        Create an empty menu.
        """
        self._entries = []
        self.width = width
        self.height = height
        self._cache = None
        self.color = color
        self.active = active
        self.bg = bg

        self._chars = 'abcdefghijklmnopqrstuvwxyz0123456789!?# ()[].,-_:;+='
        self._font = Image.open('pymlgame/font.png').convert('RGB')
        self.selected_entry = -1

    def add_entry(self, text, callback=None):
        """
        Add a menu entry to the end and return the id.
        """
        # create a surface to fit the entries text
        normal = pymlgame.Surface(len(text) * 5 + len(text) - 1, 5)

        # blit every char of the text on the entries surfaces (normal & active)
        for i in range(len(text)):
            normal.blit(self._get_char(text[i]), (i * 5 + i, 0))
        active = normal.replace_color(self.color, self.active)

        # add the new menu entry to the menu
        self._entries.append([text, normal, active, callback])

        # if this was the first item select it
        if len(self._entries) == 1:
            self.selected_entry = 0

        return len(self._entries) - 1

    def del_entry(self, i):
        """
        Removes an entry from the menu.
        """
        if self._entries[i]:
            self._entries.pop(i)
        if self.selected_entry == len(self._entries):
            self.selected_entry -= 1

    def select_entry(self, i):
        """
        Select another entry. Triggers the menu to update itself.
        """
        if len(self._entries) > 0:
            if 0 < i < len(self._entries):
                self.selected_entry = i
                self._cache = None

    def update(self):
        """
        Generate menu surface if not already cached.
        """
        #TODO: let the active entry move from left to right if too long
        if not self._cache:
            self._cache = pymlgame.Surface(self.width, self.height)
            if self._entries > 0:
                surface = pymlgame.Surface(self.width,
                                           len(self._entries) * 5 +
                                           len(self._entries))
                for i in range(len(self._entries)):
                    text = self._entries[i][1]
                    if i == self.selected_entry:
                        text = self._entries[i][2]
                    surface.blit(text, (int(self.width / 2) - int(text.width / 2),
                                        i * 5 + i))
                self._cache.blit(surface, (0, int(self.height / 2) -
                                           self.selected_entry * 5 +
                                           self.selected_entry))

    def render(self):
        """
        Return the surface of the menu.
        """
        return self._cache

    def _get_char(self, char):
        """
        Generates a surface for the given char and returns it.
        """
        surface = pymlgame.Surface(5, 5)
        if char in self._chars:
            pos = self._chars.find(char.lower())
            x = int(pos / 8)
            y = pos % 8
            for x in range(x * 5, (x + 1) * 5 + 1):
                for y in range(y * 5, (y + 1) * 5 + 1):
                    if self._font.getpixel((x, y)) == pymlgame.BLACK:
                        surface.matrix[x][y] = self.color
                    else:
                        surface.matrix[x][y] = self.bg
        else:
            surface.matrix = [[self.bg, self.bg, self.bg, self.bg, self.bg],
                              [self.bg, self.color, self.color, self.color,
                               self.bg],
                              [self.bg, self.color, self.bg, self.color,
                               self.bg],
                              [self.bg, self.color, self.color, self.color,
                               self.bg],
                              [self.bg, self.bg, self.bg, self.bg, self.bg]]
        return surface