# -*- coding: utf-8 -*-

"""
pymlgame - Font
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import os

from PIL import Image

import pymlgame


class Font(object):
    """
    Represents a font object with text on it. It's similar to a surface.
    """
    def __init__(self, text, foreground, background, brightness=0.1):
        """
        Create a surface with given text and coloring.

        @type  text: str
        @param text: The text that should be rendered.
        @type  foreground: (int, int, int)
        @param foreground: (r, g, b) values for text color.
        @type  background: (int, int, int)
        @param background: (r, g, b) values for background color.
        @type  brightness: float
        @param brightness: Adjust the brightness of the colors.
        """
        self.text = text
        self.font = 'font5x5.png'
        self._chars = 'abcdefghijklmnopqrstuvwxyz0123456789!?# ()[].,' \
                      '-_:;+=H><*~\'"/\\%°'
        self.foreground = foreground
        self.background = background
        self.brightness = brightness
        self.surface = self.update

    def update(self):
        """
        Generates the surface out of the given text.

        @rtype:  pymlgame.Surface
        @return: The generated surface of the text.
        """
        #TODO: make multiline text possible
        surface = pymlgame.Surface(len(self.text) * 5 + len(self.text), 5)
        surface.fill(self.background, self.brightness)

        for i in range(len(self.text)):
            surface.blit(self._read_char(self.text[i]), (i * 5 + i, 0))

        return surface

    def _read_char(self, char):
        """
        Returns a surface with the rendered char.

        @rtype:  pymlgame.Surface
        @return: The generated surface of the char.
        @type  char: str
        @param char: The char that should be read from the font file.
        @rtype:  pymlgame.Surface
        @return: The surface of the rendered char.
        """
        surface = pymlgame.Surface(5, 5)
        char_pos = self._chars.find(char) + 1
        char_x = (char_pos % 8) * 5 + (char_pos % 8)
        char_y = int(char_pos / 8) * 5 + int(char_pos / 8)
        img = Image.open(os.path.join('pymlgame', self.font))
        matrix = img.load()
        for x in range(5):
            for y in range(5):
                if matrix[x + char_x, y + char_y] == pymlgame.BLACK:
                    surface.matrix[x][y] = self.foreground
                else:
                    surface.matrix[x][y] = self.background

        return surface