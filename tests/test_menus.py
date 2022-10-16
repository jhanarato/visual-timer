from vtimer.menus import Menu, MenuOption, NOT_AN_OPTION_VALUE, NOT_A_KEY_NUMBER


def test_create_menu():
    menu = Menu()
    assert len(menu.options) == 0
    