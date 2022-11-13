from fake_keypad import FakeKeypad
from vtimer import events
import vtimer

from test_events import reset_subscriptions
from vtimer.events import EventHandler
from vtimer.actions import PressEmitter, enable_keypress_action


def test_post_and_subscribe(reset_subscriptions):
    handler = EventHandler("event")
    events.post_event("event", 123)
    assert handler.event == 123


def test_keypress_event_emitted(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    key = vtimer.keypad.keys[10]

    handler = EventHandler("keypress")
    emitter = PressEmitter()
    enable_keypress_action(emitter)

    key.press()
    vtimer.keypad.update()

    assert handler.event == 10
