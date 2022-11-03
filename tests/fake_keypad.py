from vtimer.keypad_interface import KeypadInterface
import vtimer.menus
import vtimer.events


class TooManyUpdatesError(Exception):
    def __init__(self, maximum, number):
        self.maximum = maximum
        self.number = number


class FakeKey:
    def __init__(self, number):
        self.number = number
        self.rgb = None
        self.keypress_handler = None
        self.keyhold_handler = None

    def press(self):
        self.keypress_handler(self)

    def hold(self):
        self.keyhold_handler(self)


class FakeKeypad:
    def __init__(self, number_of_keys=16, max_updates=1):
        self.keys = [FakeKey(number) for number in range(0, number_of_keys)]
        self.number_of_updates = 0
        self.max_updates = max_updates

    def set_keypress_function(self, key_num, fn):
        self.keys[key_num].keypress_handler = fn

    def set_keyhold_function(self, key_num, fn):
        self.keys[key_num].keyhold_handler = fn

    def set_key_colour(self, key_num, colour):
        self.keys[key_num].rgb = colour

    def set_all_keys_colour(self, colour):
        for key in self.keys:
            key.rgb = colour

    def update(self):
        vtimer.events.post_event("menu_selection_made", vtimer.menus.SelectionMadeEvent(10))

        self.number_of_updates += 1
        if self.number_of_updates > self.max_updates:
            raise TooManyUpdatesError(self.max_updates, self.number_of_updates)
