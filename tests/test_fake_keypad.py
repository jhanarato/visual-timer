import pytest

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