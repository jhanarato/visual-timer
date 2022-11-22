from fake_keypad import FakeKeypad, FakeKey
from vtimer import events
import vtimer

from test_events import reset_subscriptions
from vtimer.events import EventHandler
from vtimer.actions import KeypressEmitter, KeyListener
from vtimer.actions import KEYPRESS_EVENT, ANY_KEYPRESS_EVENT


def test_keypress_event_emitted(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    key = vtimer.keypad.keys[10]

    handler = EventHandler(KEYPRESS_EVENT)
    emitter = KeypressEmitter()

    key.press()
    vtimer.keypad.update()

    assert handler.event == 10


def test_keypress_listener_press_handled(reset_subscriptions):
    listener = KeyListener()
    emitter = KeypressEmitter()
    emitter.invoke_press(FakeKey(0))
    assert listener.key_pressed


def test_key_listener_hold(reset_subscriptions):
    listener = KeyListener()
    emitter = KeypressEmitter()
    emitter.invoke_hold(FakeKey(0))
    assert listener.key_held