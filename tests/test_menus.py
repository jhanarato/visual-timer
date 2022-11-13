import pytest

from test_events import reset_subscriptions
from vtimer.events import EventHandler

from vtimer.menus import Menu, MenuOption, TooManyOptionsError, MENU_SELECTION_EVENT
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
    with pytest.raises(TooManyOptionsError) as excinfo:
        menu = Menu(number_of_keys=0)
        menu.options = [MenuOption(0, "blue", 7)]
    assert excinfo.value.number_of_options == 16


def test_making_selection_posts_event(reset_subscriptions):
    handler = EventHandler(MENU_SELECTION_EVENT)
    menu = Menu()
    menu.options = [MenuOption(0, "blue", 3)]
    menu.select(0)

    selected_option = handler.event.option
    assert selected_option.value == 3


def test_can_create_menu_with_name():
    menu = Menu(name="a_name")
