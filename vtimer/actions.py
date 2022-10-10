from vtimer.util import keypad, rotated_key_num
from vtimer.menus import NOT_A_KEY_NUMBER


def enable_keypress_action(action):
    for key in keypad.keys:
        key.press_function = action.invoke


def enable_hold_action(action):
    for key in keypad.keys:
        key.hold_function = action.invoke


class NextViewAction:
    def __init__(self, view_cycle):
        self.view_cycle = view_cycle

    def invoke(self, key):
        self.view_cycle.advance()


class CancelAction:
    def __init__(self, timer):
        self._timer = timer

    def invoke(self, key):
        self._timer.cancelled = True


class OptionSelectAction:
    def __init__(self, menu):
        self._menu = menu
        self.selected_key_num = NOT_A_KEY_NUMBER

    def invoke(self, key):
        self.selected_key_num = rotated_key_num[key.number]

    def wait_for_selection(self):
        while not self._menu.selection_made:
            if self._menu.option_valid_at_key(self.selected_key_num):
                self._menu.select(self.selected_key_num)
            keypad.update()


class KeypressWaitAction:
    def __init__(self):
        self._pressed = False

    def invoke(self, key):
        self._pressed = True

    def wait(self):
        while not self._pressed:
            keypad.update()
