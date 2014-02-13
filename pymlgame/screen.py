# -*- coding: utf-8 -*-

"""
pymlgame - Screen
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import socket

import pymlgame


class Screen(object):
    """
    Represents the Mate Light screen and has all the drawing methods.
    """
    def __init__(self, host, port, width=40, height=16):
        """
        Create a screen with default size and fill it with black pixels.

        @type  host: str
        @param host: Hostname or IP address of the Mate Light screen.
        @type  port: int
        @param port: Port of the Mate Light screen.
        @type  width: int
        @param width: The width in bottles of the Mate Light screen.
        @type  height: int
        @param height: The height in bottles of the Mate Light screen.
        """
        self.host = host
        self.port = port
        self.width = width
        self.height = height

        self.matrix = None
        self.reset()

    def reset(self):
        """
        Fill the screen with black pixels.
        """
        surface = pymlgame.Surface(self.width, self.height)
        surface.fill(pymlgame.BLACK)
        self.matrix = surface.matrix

    def update(self):
        """
        Sends the current screen contents to Mate Light.
        """
        display_data = []
        for y in range(self.height):
            for x in range(self.width):
                for color in self.matrix[x][y]:
                    display_data.append(int(color))

        checksum = bytearray([0, 0, 0, 0])
        data_as_bytes = bytearray(display_data)
        data = data_as_bytes + checksum
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (self.host, self.port))

    def blit(self, surface, pos=(0, 0)):
        """
        Blits a surface on the screen at pos.

        @type  surface: pymlgame.Surface
        @param surface: The surface that will be blitted.
        @type  pos: (int, int)
        @param pos: (x, y) coordinates where the upper left corner of
                    the surface should be placed.
        """
        for x in range(surface.width):
            for y in range(surface.height):
                point = (x + pos[0], y + pos[1])
                if self.point_on_screen(point):
                    self.matrix[point[0]][point[1]] = surface.matrix[x][y]

    def point_on_screen(self, pos):
        """
        Checks if the given point is outside of the visible area of the screen.

        @type  pos: (int, int)
        @param pos: (x, y) coordinates of the point to check.
        @rtype: bool
        @return: Return True if the point in in the visible area and False if
                 it's not.
        """
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            return True
        else:
            return False