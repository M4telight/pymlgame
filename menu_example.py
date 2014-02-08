#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-

"""
pymlgame example game
"""

__author__ = "Ricardo Band"
__copyright__ = "Copyright 2013, Ricardo Band"
__credits__ = ["Ricardo Band"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Ricardo Band"
__email__ = "me@xengi.de"
__status__ = "Development"

import pymlgame


class Game(object):
    """
    The main game class that holds the gameloop
    """
    def __init__(self, host, port, width, height):
        """
        Create a screen and define some game specific things
        """
        self.screen = pymlgame.Screen(host, port, width, height)
        self.clock = pymlgame.Clock()
        self.running = True
        self.menu = pymlgame.Menu(width, height, pymlgame.WHITE, pymlgame.CYAN,
                                  pymlgame.BLACK)
        self.menu.add_entry('new game')
        self.menu.add_entry('options')
        self.menu.add_entry('quit')

    def update(self):
        """
        Update the screens contents in every loop
        """
        self.menu.update()

    def render(self):
        """
        Send the current screen content to Mate Light
        """
        self.screen.reset()
        self.screen.blit(self.menu.render())

        self.screen.update()
        self.clock.tick(10)

    def handle_events(self):
        """
        Loop through all events
        """
        pass

    def gameloop(self):
        """
        A game loop that circles through the methods
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    GAME = Game('127.0.0.1', 1337, 40, 40)
    GAME.gameloop()