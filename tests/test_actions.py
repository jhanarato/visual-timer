from fake_keypad import FakeKeypad
from vtimer import events
import vtimer

from test_events import reset_subscriptions
from vtimer.events import EventHandler
from vtimer.actions import PressEmitter, enable_keypress_action
from vtimer.actions import KEYPRESS_EVENT, ANY_KEYPRESS_EVENT


def test_keypress_event_emitted(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    key = vtimer.keypad.keys[10]

    handler = EventHandler(KEYPRESS_EVENT)
    emitter = PressEmitter()

    key.press()
    vtimer.keypad.update()

    assert handler.event == 10


def test_any_key_event_emitted(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    key = vtimer.keypad.keys[10]

    handler = EventHandler(ANY_KEYPRESS_EVENT)
    emitter = PressEmitter()

    key.press()
    vtimer.keypad.update()

    assert handler.event