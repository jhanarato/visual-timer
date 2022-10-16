class Keypad:
    def __init__(self, pmk):
        self._pmk = pmk

    def set_keypress_function(self, key_num, fn):
        key = self._pmk.keys[key_num]
        key.press_function = fn

    def set_keyhold_function(self, key_num, fn):
        key = self._pmk.keys[key_num]
        key.hold_function = fn

    def set_led_colour(self, key_num, colour):
        self._pmk.keys[key_num].set_led(*colour)

    def set_all_keys_colour(self, colour):
        self._pmk.set_all(*colour)

    def update(self):
        self._pmk.update()
