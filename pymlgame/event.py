# -*- coding: utf-8 -*-

"""
PyMLGame - Event
"""

from pymlgame.locals import E_KEYDOWN, E_KEYUP, E_KEYPRESSED


class Event(object):
    def __init__(self, uid, type, data=None):
        self.uid = uid
        self.type = type
        if type in [E_KEYDOWN, E_KEYUP, E_KEYPRESSED]:
            self.button = data
        else:
            self.data = data
