import pytest

from test_events import reset_subscriptions

from vtimer.menus import Menu, MenuOption, TooManyOptionsError, SelectionMadeEvent
from vtimer import events


def test_create_menu():
    menu = Menu()
    assert len(menu.options) == 0


def test_select_valid_option():
    menu = Menu()
    menu.options = [MenuOption(0, "blue", 7)]
    menu.select(0)
    assert menu.selection_made


def test_select_missing_option():
    menu = Menu()
    menu.options = [MenuOption(0, "blue", 7)]
    menu.select(1)
    assert not menu.selection_made


def test_too_many_options():
    with pytest.raises(TooManyOptionsError):
        menu = Menu(number_of_keys=0)
        menu.options = [MenuOption(0, "blue", 7)]


def test_making_selection_posts_event(reset_subscriptions):
    captured_event = None

    def select_handler(posted_event):
        nonlocal captured_event
        captured_event = posted_event

    events.subscribe("menu_selection_made", select_handler)

    menu = Menu()
    menu.options = [MenuOption(0, "blue", 3)]
    menu.select(0)

    assert captured_event.value_selected == 3
