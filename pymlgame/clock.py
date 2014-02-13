# -*- coding: utf-8 -*-

"""
pymlgame - Clock
"""

__author__ = 'Ricardo Band'
__copyright__ = 'Copyright 2014, Ricardo Band'
__credits__ = ['Ricardo Band']
__license__ = 'MIT'
__version__ = '0.1.1'
__maintainer__ = 'Ricardo Band'
__email__ = 'me@xengi.de'
__status__ = 'Development'

import time


class Clock(object):
    """
    Measure the time to adjust drawing rates.
    """
    def __init__(self):
        """
        Get a fresh Clock.
        """
        pass

    def tick(self, fps):
        """
        Let the Clock tick x times per second.

        @type  fps: int
        @param fps: The frame rate that you want.
        """
        time.sleep(1.0/fps)