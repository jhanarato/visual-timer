from vtimer.keypad_interface import KeypadInterface
import vtimer.menus
import vtimer.events


class FakeKeypad:
    def __init__(self):
        pass

    def set_keypress_function(self, key_num, fn):
        raise NotImplementedError(not_implemented_message + "set_keypress_function")

    def set_keyhold_function(self, key_num, fn):
        raise NotImplementedError(not_implemented_message + "set_keyhold_function")

    def set_key_colour(self, key_num, colour):
        raise NotImplementedError(not_implemented_message + "set_led_colour")

    def set_all_keys_colour(self, colour):
        raise NotImplementedError(not_implemented_message + "set_all_keys_colour")

    def update(self):
        vtimer.events.post_event("menu_selection_made", vtimer.menus.SelectionMadeEvent(10))