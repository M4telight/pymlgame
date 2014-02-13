#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
pymlgame - controller example
=============================

This example shows how you can use a controller connected to a laptop or any
other machine capable of pygame to connect to a pymlgame instance.
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import sys

import pygame
import jsonrpclib


class Controller(object):
    def __init__(self, host, port, v=False):
        """
        Create game that takes controller inputs and emits JSONRPC calls.

        @type  host: str
        @param host: Hostname or IP address.
        @type  port: int
        @param port: Port number of pymlgame.
        @type  v: bool
        @param v: Turn verbosity on or off.
        """
        self.host = host
        self.port = port
        self.v = v
        pygame.init()
        self.joysticks = [[pygame.joystick.Joystick(j), None, None]
                          for j in range(pygame.joystick.get_count())]
        self.screen = pygame.display.set_mode((100, 10))
        pygame.display.set_caption("pymlgame_ctlr")
        self.clock = pygame.time.Clock()
        self.server = jsonrpclib.Server('http://' + self.host + ':' +
                                        str(self.port))
        foundone = False
        for joy in self.joysticks:
            joy[0].init()
            joy[1] = self.server.init()
            # define some mappings for compatible controllers
            # for now only the XBOX 360 Wireless Controller is supported
            if joy[0].get_name() == 'Xbox 360 Wireless Receiver':
                joy[2] = {0: 'A',
                          1: 'B',
                          2: 'X',
                          3: 'Y',
                          4: 'L1',
                          5: 'R1',
                          6: 'Select',
                          7: 'Start',
                          11: 'Left',
                          12: 'Right',
                          13: 'Up',
                          14: 'Down'}
                foundone = True
            else:
                print('Sorry but this Controller is not supported yet. (',
                      joy[0].get_name(), ')')

        if not foundone:
            print('Sorry no compatible controllers found on your system.')
            self.quit(0)

    def handle_events(self):
        """
        Gets events from pygame and checks if there is some interesting like
        pressed controller buttons.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.v:
                    print('joy', self.joysticks[event.joy][0].get_name(),
                          '(uid:', self.joysticks[event.joy][1],
                          ')button pressed:', event.button)
                self.server.trigger_button(self.joysticks[event.joy][1],
                                           'KeyDown',
                                           self.joysticks[event.joy][2][event.button])
            elif event.type == pygame.JOYBUTTONUP:
                if self.v:
                    print('joy', self.joysticks[event.joy][0].get_name(),
                          '(uid:', self.joysticks[event.joy][1],
                          ')button released:', event.button)
                self.server.trigger_button(self.joysticks[event.joy][1],
                                           'KeyUp',
                                           self.joysticks[event.joy][2][event.button])

    def update(self):
        """
        This thing doesn't do anything.
        """
        pass

    def render(self):
        """
        Updates the screen and sends it to the output.
        """
        pygame.display.update()
        pygame.display.flip()

    def gameloop(self):
        """
        Contains the mainloop which runs the whole game.
        """
        try:
            while True:
                self.handle_events()
                self.update()
                self.render()
        except KeyboardInterrupt:
            pass

        self.quit(0)

    def quit(self, exitcode=0):
        """
        Correctly exit all this stuff.

        @type  exitcode: int
        @param exitcode: The exit code i.e. 0 for clean exit.
        """
        pygame.joystick.quit()
        pygame.quit()
        sys.exit(exitcode)


if __name__ == '__main__':
    CTLR = Controller('127.0.0.1', 1338, True if '-v' in sys.argv else False)
    CTLR.gameloop()