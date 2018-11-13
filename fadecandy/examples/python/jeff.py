#!/usr/bin/python

import time, random
from . import opc
from functools import reduce


BLOXL_HOST = 'localhost'
BLOXL_PORT = '7890'


def get_client():
    return opc.Client('{0}:{1}'.format(BLOXL_HOST, BLOXL_PORT))


NUMBER_LEDS = 800
NUMBER_ROWS = 20
NUMBER_COLUMNS = 10
NUMBER_LEDS_PER_SQ = 4

HIDDEN_PIXEL = (0, 0, 0)


TINY_DELAY = 0.05
SHORT_DELAY = 0.1
MEDIUM_DELAY = 0.3
LONG_DELAY = 0.5
LONGER_DELAY = 0.8
LONGEST_DELAY = 1.5


def delay(t=None):
    if t:
        time.sleep(t)


def wheel(WheelPos):
    if WheelPos < 85:
        color = ((WheelPos * 3), (255 - WheelPos * 3), 0)
        return color
    else:
        if WheelPos < 170:
            WheelPos -= 85
            color = ((255 - WheelPos * 3), 0, (WheelPos * 3))
            return color
        else:
            WheelPos -= 170
            color = (0, (WheelPos * 3), (255 - WheelPos * 3))
            return color


def flatten_list(lst):
    return reduce(lambda x, y: x + y, lst)


class Bloxl(object):

    DEFAULT_DELAY_BEFORE = None
    DEFAULT_DELAY = SHORT_DELAY

    def __init__(self):

        self.client = get_client()

        self.grid = [[SqBlox(rownum, colnum) for colnum in range(NUMBER_COLUMNS)] for rownum in range(NUMBER_ROWS)]

    def get_flat_pixels(self):
        return flatten_list([sq.get_pixels() for sq in flatten_list(self.grid)])

    def get_flat_colors(self):
        return flatten_list([sq.get_colors() for sq in flatten_list(self.grid)])

    def display(self, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        if display:
            delay(delay_before)
            self.client.put_pixels(self.get_flat_pixels())
            delay(delay_after)

    def blanket_pixels(self, pixels=None, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for led in self.leds:
            led.set_pixels(pixels)
        self.display(display, delay_after, delay_before)

    def blanket_color(self, color, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for led in self.leds:
            led.set_color(color)
        self.display(display, delay_after, delay_before)

    def hide_all(self, display=True, delay_after=DEFAULT_DELAY, delay_before=DEFAULT_DELAY_BEFORE):
        for sq in self.grid:
            sq.hide()
        self.display(display, delay_after, delay_before)


class SqBlox(object):

    def __init__(self, rownum, colnum):

        self.leds = [LedBlox(sqnum, rownum, colnum) for sqnum in range(NUMBER_LEDS_PER_SQ)]

    def get_pixels(self):
        return [e.pixels for e in self.leds]

    def get_colors(self):
        return [e.color_val for e in self.leds]

    def blanket_pixels(self, pixels=None):
        for led in self.leds:
            led.set_pixels(pixels)

    def blanket_color(self, color):
        for led in self.leds:
            led.set_color(color)

    def hide_all(self):
        for led in self.leds:
            led.hide()

    def is_hidden(self):
        for led in self.leds:
            if led.is_hidden():
                return True
        return False


class LedBlox(object):

    def __init__(self, sqnum, rownum, colnum, pixels=None, color=None, wheel_val=None):

        self.sqnum = sqnum
        self.rownum = rownum
        self.colnum = colnum

        self.pixels = None
        self.set_pixels(pixels)

        self.color_val = None
        self.set_color(color)

    def set_color(self, color=None):
        if color:
            self.color_val = color
            self.set_pixels(wheel(color))

    def set_pixels(self, pixels=None):
        if pixels:
            self.pixels = pixels

    def hide(self):
        self.set_pixels(pixels=HIDDEN_PIXEL)

    def is_hidden(self):
        return self.pixels == HIDDEN_PIXEL


