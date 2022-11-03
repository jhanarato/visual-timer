import vtimer.menus
import vtimer.waiting
import vtimer.events

from fake_keypad import FakeKeypad
from test_events import reset_subscriptions


def test_wait_for_selection_ends_on_menu_event(reset_subscriptions):
    vtimer.keypad = FakeKeypad()
    menu = vtimer.menus.Menu()
    menu.options = [vtimer.menus.MenuOption(0, "blue", 7)]
    vtimer.waiting.wait_for_selection(menu)


