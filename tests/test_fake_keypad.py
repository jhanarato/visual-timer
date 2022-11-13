import pytest

import fake_keypad
from fake_keypad import FakeKeypad

import vtimer.util


def test_set_one_key_colour():
    keypad = FakeKeypad()
    keypad.set_key_colour(0, vtimer.util.key_colours["red"])
    assert keypad.keys[0].rgb == (255, 0, 0)


def test_set_two_key_colour():
    keypad = FakeKeypad()
    keypad.set_key_colour(0, vtimer.util.key_colours["red"])
    keypad.set_key_colour(1, vtimer.util.key_colours["blue"])
    assert keypad.keys[0].rgb == (255, 0, 0)
    assert keypad.keys[1].rgb == (0, 0, 255)


def test_set_many_colours():
    keypad = FakeKeypad()
    for key_num in range(0, 11):
        keypad.set_key_colour(key_num, vtimer.util.key_colours["red"])

    for key in keypad.keys:
        key.rgb = (255, 0, 0)


def test_set_each_key_in_all_keys_set():
    keypad = FakeKeypad()
    for key_num in vtimer.util.all_keys:
        keypad.set_key_colour(key_num, vtimer.util.key_colours["red"])

    for key in keypad.keys:
        assert key.rgb == (255, 0, 0)


def test_set_all_keys_colour():
    keypad = FakeKeypad()
    keypad.set_all_keys_colour(vtimer.util.key_colours["red"])

    for key in keypad.keys:
        assert key.rgb == (255, 0, 0)


def test_set_keypress_function():
    key_num_pressed = None

    def handler(key):
        nonlocal key_num_pressed
        key_num_pressed = key.number

    keypad = FakeKeypad()
    keypad.set_keypress_function(7, handler)
    keypad.keys[7].press()
    keypad.update()

    assert key_num_pressed == 7


def test_set_keyhold_function():
    key_num_held = None

    def handler(key):
        nonlocal key_num_held
        key_num_held = key.number

    keypad = FakeKeypad()
    keypad.set_keyhold_function(2, handler)
    keypad.keys[2].hold()
    keypad.update()

    assert key_num_held == 2


def test_number_of_updates():
    keypad = FakeKeypad(max_updates=2)
    keypad.update()
    assert keypad.number_of_updates == 1
    keypad.update()
    assert keypad.number_of_updates == 2


def test_too_many_updates():
    keypad = FakeKeypad(max_updates=2)
    keypad.update()
    keypad.update()

    with pytest.raises(fake_keypad.MaxUpdatesException):
        keypad.update()


def test_press_key():
    def press_handler(key):
        pass

    keypad = FakeKeypad()
    keypad.set_keypress_function(0, press_handler)

    _key = keypad.keys[0]

    assert not _key.pressed
    _key.press()
    assert _key.pressed
    keypad.update()
    assert not _key.pressed


def test_hold_key():
    def hold_handler(key):
        pass

    keypad = FakeKeypad()
    keypad.set_keyhold_function(0, hold_handler)

    _key = keypad.keys[0]

    assert not _key.held
    _key.hold()
    assert _key.held
    keypad.update()
    assert not _key.held


def test_call_keypress_handler_on_update():
    key_num = 5

    key_pressed = None

    def press_handler(key):
        nonlocal key_pressed
        key_pressed = key

    keypad = FakeKeypad()
    keypad.set_keypress_function(key_num, press_handler)

    keypad.keys[key_num].press()
    keypad.update()

    assert key_pressed.number == key_num


def test_call_keyhold_handler_on_update():
    key_num = 5

    key_held = None

    def hold_handler(key):
        nonlocal key_held
        key_held = key

    keypad = FakeKeypad()
    keypad.set_keyhold_function(key_num, hold_handler)

    keypad.keys[key_num].hold()
    keypad.update()

    assert key_held.number == key_num


def test_handler_not_called_if_not_pressed():
    key_pressed = None

    def press_handler(key):
        nonlocal key_pressed
        key_pressed = key

    keypad = FakeKeypad()
    keypad.set_keypress_function(0, press_handler)

    keypad.update()

    assert key_pressed is None


def test_event_15_problem():
    not_15 = 14

    key_pressed = None

    def press_handler(key):
        nonlocal key_pressed
        key_pressed = key

    vtimer.keypad = FakeKeypad()

    for key_num in vtimer.util.all_keys:
        vtimer.keypad.set_keypress_function(key_num, press_handler)

    key = vtimer.keypad.keys[not_15]
    key.press()
    vtimer.keypad.update()

    assert key_pressed.number == not_15
