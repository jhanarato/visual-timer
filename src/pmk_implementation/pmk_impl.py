from pmk.platform.keybow2040 import Keybow2040
from pmk import PMK


class Keypad:
    def __init__(self, pmk):
        self._pmk = pmk

    def set_keypress_function(self, key_num, fn):
        key = self._pmk.keys[key_num]
        key.press_function = fn

    def set_keyhold_function(self, key_num, fn):
        key = self._pmk.keys[key_num]
        key.hold_function = fn

    def set_key_colour(self, key_num, colour):
        self._pmk.keys[key_num].set_led(*colour)

    def set_all_keys_colour(self, colour):
        self._pmk.set_all(*colour)

    def update(self):
        self._pmk.update()


def get_keypad():
    keybow2040 = Keybow2040()
    pmk = PMK(keybow2040)
    return Keypad(pmk)
