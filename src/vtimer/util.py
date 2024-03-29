# Import libraries for Pimoroni Mechanical Keypad
import time
import vtimer

all_keys = frozenset(range(0, 16))

rotated_key_num = [0, 4, 8,  12,
                   1, 5, 9,  13,
                   2, 6, 10, 14,
                   3, 7, 11, 15]


key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "cyan": (0, 255, 255),
               "orange": (255, 165, 0),
               "none": (0, 0, 0)}


def cycle(iterable):
    """ A simple implementation of itertools.cycle() """
    while True:
        for element in iterable:
            yield element


def partial(func, *args, **keywords):
    """ An implementation of functools.partial() from the Adafruit website"""
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    return newfunc


def set_key_colour(key_num, colour):
    key_num = rotated_key_num.index(key_num)
    vtimer.keypad.set_key_colour(key_num, key_colours[colour])


def set_all_keys_colour(colour):
    vtimer.keypad.set_all_keys_colour(key_colours[colour])


class Pause:
    def __init__(self, seconds):
        self._seconds_to_pause_for = seconds
        self._start = time.monotonic()

    def complete(self):
        now = time.monotonic()
        paused_for = now - self._start
        return paused_for > self._seconds_to_pause_for

    def wait_until_complete(self):
        while not self.complete():
            vtimer.keypad.update()
