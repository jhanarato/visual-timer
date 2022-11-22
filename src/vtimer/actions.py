import vtimer
from vtimer import events
from vtimer.util import rotated_key_num, all_keys

KEYPRESS_EVENT = "keypress"
KEYHOLD_EVENT = "keyhold"
ANY_KEYPRESS_EVENT = "any-keypress"

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


class KeypressEmitter:
    def __init__(self):
        for key_num in all_keys:
            vtimer.keypad.set_keypress_function(key_num, self.invoke_press)

        for key_num in all_keys:
            vtimer.keypad.set_keyhold_function(key_num, self.invoke_hold)

    def invoke_press(self, key):
        events.post_event(KEYPRESS_EVENT, key.number)
        events.post_event(ANY_KEYPRESS_EVENT, key.number)

    def invoke_hold(self, key):
        events.post_event(KEYHOLD_EVENT, key.number)


class KeyListener:
    def __init__(self):
        self.key_pressed = False
        self.any_key_pressed = False
        self.key_held = False

        self.subscribe()

    def subscribe(self):
        events.subscribe(KEYPRESS_EVENT, self.on_keypress)
        events.subscribe(ANY_KEYPRESS_EVENT, self.on_any_keypress)
        events.subscribe(KEYHOLD_EVENT, self.on_keyhold)

    def on_keypress(self, key_num):
        self.key_pressed = True

    def on_any_keypress(self, key_num):
        self.any_key_pressed = True

    def on_keyhold(self, key_num):
        self.key_held = True
