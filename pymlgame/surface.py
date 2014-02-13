# -*- coding: utf-8 -*-

"""
pymlgame - Surface
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


class Surface(object):
    """
    Represents a sheet to draw on
    """
    def __init__(self, width, height):
        """
        Create a surface with default size and fill it with black pixels.

        @type  width: int
        @param width: The width in bottles of the new Surface.
        @type  height: int
        @param height: The height in bottles of the new Surface.
        """
        self.width = width
        self.height = height
        self.matrix = None
        self.fill(pymlgame.BLACK)

    def fill(self, color, brightness=0.1):
        """
        Fill the whole screen with the given color.

        @type  color: (int, int, int)
        @param color: The color which will fill the surface.
        @type  brightness: float
        @param brightness: Adjust the colors by this brightness level.
        """
        color = self.get_color(color, brightness)
        self.matrix = [[color for _ in range(self.height)]
                       for _ in range(self.width)]

    def draw_dot(self, pos, color, brightness=0.1):
        """
        Draw one single dot with the given color on the screen.

        @type  pos: (int, int)
        @param pos: (x, y) coordinates where the dot should be placed.
        @type  color: (int, int, int)
        @param color: The color of the dot.
        @type  brightness: float
        @param brightness: Adjust the colors by this brightness level.
        """
        realcolor = self.get_color(color, brightness)
        if 0 <= pos[0] < self.width and 0 <= pos[1] < self.height:
            self.matrix[pos[0]][pos[1]] = realcolor

    def draw_line(self, start, end, color, brightness=0.1):
        """
        Draw a line with the given color on the screen.

        @type  start: (int, int)
        @param start: (x, y) coordinates where the line should start.
        @type  end: (int, int)
        @param end: (x, y) coordinates where the line should end.
        @type  color: (int, int, int)
        @param color: The color of the line.
        @type  brightness: float
        @param brightness: Adjust the colors by this brightness level.
        """
        def dist(p, a, b):
            return abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) *
                       (b[1] - a[1])) / math.sqrt((b[0] - a[0])**2 +
                                                  (b[1] - a[1])**2)

        points = []
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                if dist((x, y), start, end) < 0.5:
                    points.append((x, y))
        for point in points:
            self.draw_dot(point, color, brightness)

    def draw_rect(self, pos, size, color, fillcolor=None, brightness=0.1):
        """
        Draw a rectangle with the given color on the screen and optionally fill
        it with fillcolor.

        @type  pos: (int, int)
        @param pos: (x, y) coordinates where the upper left corner of the
                    rectangle should be placed.
        @type  size: (int, int)
        @param size: The width and height of the rectangle that will be
                     created.
        @type  color: (int, int, int)
        @param color: The border color of the rectangle.
        @type  fillcolor: (int, int, int)
        @param fillcolor: The inner color of the rectangle.
        @type  brightness: float
        @param brightness: Adjust the colors by this brightness level.
        """
        # draw top and botton line
        for x in range(size[0]):
            self.draw_dot((pos[0] + x, pos[1]), color, brightness)
            self.draw_dot((pos[0] + x, pos[1] + size[1] - 1), color, brightness)
        # draw left and right side
        for y in range(size[1]):
            self.draw_dot((pos[0], pos[1] + y), color, brightness)
            self.draw_dot((pos[0] + size[0] - 1, pos[1] + y), color, brightness)
        # draw filled rect
        #TODO: find out if the rect is at least 3x3 to actually have a filling
        if fillcolor:
            for x in range(size[0] - 2):
                for y in range(size[1] - 2):
                    self.draw_dot((pos[0] + 1 + x, pos[1] + 1 + y),
                                  fillcolor, brightness)

    def draw_circle(self, pos, radius, color, fillcolor=None, brightness=0.1):
        """
        Draw a circle with the given color on the screen and optionally fill it
        with fillcolor.

        @type  pos: (int, int)
        @param pos: (x, y) coordinates where the upper left corner of the
                    circle should be placed.
        @type  radius: int
        @param radius: The radius of the circle that will be created.
        @type  color: (int, int, int)
        @param color: The border color of the circle.
        @type  fillcolor: (int, int, int)
        @param fillcolor: The inner color of the circle.
        @type  brightness: float
        @param brightness: Adjust the colors by this brightness level.
        """
        #TODO: This still produces rubbish but it's on a good way to success
        def dist(d, p, r):
            return abs(math.sqrt((p[0] - d[0])**2 + (p[1] - d[1])**2) - r)

        points = []
        for x in range(pos[0] - radius, pos[0] + radius):
            for y in range(pos[1] - radius, pos[1] + radius):
                if 0 < x < self.width and 0 < y < self.height:
                    if dist((x, y), pos, radius) < 1.3:
                        points.append((x, y))

        # draw fill color
        if fillcolor:
            for point in points:
                pass
        # draw outline
        for point in points:
            self.draw_dot(point, color, brightness)

    def blit(self, surface, pos=(0, 0)):
        """
        Blits a surface on this surface at pos

        @type  surface: pymlgame.Surface
        @param surface: The surface that will be blitted.
        @type  pos: (int, int)
        @param pos: (x, y) coordinates where the upper left corner of
                    the surface should be placed.
        """
        for x in range(surface.width):
            for y in range(surface.height):
                px = x + pos[0]
                py = y + pos[1]
                if 0 < px < self.width and 0 < py < self.height:
                    self.matrix[px][py] = surface.matrix[x][y]

    def replace_color(self, before, after):
        """
        Replaces a color on a surface with another one.

        @type  before: (int, int, int)
        @param before: The color that should be changed.
        @type  after: (int, int, int)
        @param after: The color which will replace the old one.
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.matrix[x][y] == before:
                    self.matrix[x][y] = after

    @staticmethod
    def get_color(color, brightness=0.1):
        """
        Returns the color with applied brightness level.

        @type  color: (int, int, int)
        @param color: The original color.
        @type  brightness: float
        @param brightness: The level of brightness in percent.
        @rtype: (int, int, int)
        @return: The new color with adjusted brightness.
        """
        return tuple([math.floor(val * brightness) for val in color])