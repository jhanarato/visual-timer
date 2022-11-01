from vtimer.keypad_interface import KeypadInterface
import vtimer.menus
import vtimer.events

not_implemented_message = "Implementation must be provided before calling "


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
    def __init__(self, number_of_keys=16):
        self.keys = [FakeKey(number) for number in range(0, number_of_keys)]

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