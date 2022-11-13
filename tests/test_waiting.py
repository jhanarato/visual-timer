import pytest

import vtimer

from vtimer.menus import Menu, MenuOption
from vtimer.waiting import wait_for_selection

from fake_keypad import FakeKeypad, MaxUpdatesException
from test_events import reset_subscriptions


def test_wait_for_selection_ends_on_menu_event(reset_subscriptions):
    menu = Menu()

    def press_handler(key):
        menu.select(0)

    vtimer.keypad = FakeKeypad()
    vtimer.keypad.set_keypress_function(0, press_handler)
    vtimer.keypad.keys[0].press()

    menu.options = [MenuOption(0, "blue", 7)]
    vtimer.waiting.wait_for_selection()


def test_wait_until_selection_waits(reset_subscriptions):
    menu = Menu()
    vtimer.keypad = FakeKeypad()
    with pytest.raises(MaxUpdatesException):
        vtimer.waiting.wait_for_selection()