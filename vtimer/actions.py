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


class SelectMenuOptionAction:
    def __init__(self, menu):
        self._menu = menu

    def invoke(self, key):
        self._menu.select(rotated_key_num[key.number])


def wait_for_selection(menu):
    while not menu.selection_made:
        keypad.update()


class KeypressWaitAction:
    def __init__(self):
        self._pressed = False

    def invoke(self, key):
        self._pressed = True

    def wait(self):
        while not self._pressed:
            keypad.update()
