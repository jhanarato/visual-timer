import pytest

from vtimer.menus import Menu, MenuOption, TooManyOptionsError


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

