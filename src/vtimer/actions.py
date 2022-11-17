import vtimer
from vtimer import events
from vtimer.util import rotated_key_num, all_keys

KEYPRESS_EVENT = "keypress"

def enable_keypress_action(action):
    for key_num in all_keys:
        vtimer.keypad.set_keypress_function(key_num, action.invoke)


def enable_hold_action(action):
    for key_num in all_keys:
        vtimer.keypad.set_keyhold_function(key_num, action.invoke)


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


class KeypressWaitAction:
    def __init__(self):
        self._pressed = False

    def invoke(self, key):
        self._pressed = True

    def wait(self):
        while not self._pressed:
            vtimer.keypad.update()


class PressEmitter:
    def __init__(self):
        pass

    def invoke(self, key):
        events.post_event(KEYPRESS_EVENT, key.number)
