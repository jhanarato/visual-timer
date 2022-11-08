from fake_keypad import FakeKeypad
from vtimer import events
import vtimer

from test_events import Handler, reset_subscriptions
from vtimer.actions import PressEmitter, enable_keypress_action


def test_handler(reset_subscriptions):
    handler = Handler()
    handler(123)
    assert handler.event == 123


def test_post_and_subscribe(reset_subscriptions):
    handler = Handler()
    events.subscribe("event", handler)
    events.post_event("event", 123)
    assert handler.event == 123


def test_keypress_event_emitted(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    key = vtimer.keypad.keys[15]

    handler = Handler()
    events.subscribe("keypress", handler)

    emitter = PressEmitter()
    enable_keypress_action(emitter)

    key.press()
    vtimer.keypad.update()

    # TODO: Figure out why 15 is the only number that works.
    assert handler.event == 15
