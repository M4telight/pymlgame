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

import math

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
        self.font = 'default'
        self.foreground = foreground
        self.background = background
        self.brightness = brightness
        self.surface = self.update

    def update(self):
        """
        Generates the surface out of the given text.

        @rtype:   pymlgame.Surface
        @return:  The generated surface of the text.
        """
        #TODO: make multiline text possible
        surface = pymlgame.Surface(len(self.text) * 5 + len(self.text), 5)
        surface.fill(self.background, self.brightness)

        for i in range(len(self.text)):
            char = self._read_char(self.text[i])
            surface.blit(char, (i * 5 + i, 0))

        return surface

    def _read_char(self, char):
        """
        Returns a surface with the rendered char.

        @rtype:   pymlgame.Surface
        @return:  The generated surface of the char.
        """
        with open(self.font) as font:
            surface = pymlgame.Surface(5, 5)

        return self.surface