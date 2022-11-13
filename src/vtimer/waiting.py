import vtimer
from vtimer.events import EventHandler, subscribe
from vtimer.menus import MENU_SELECTION_EVENT


def wait_for_selection(menu):
    handler = EventHandler()
    subscribe(MENU_SELECTION_EVENT, handler)

    while not handler.has_event():
        vtimer.keypad.update()
