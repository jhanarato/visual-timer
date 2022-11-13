import vtimer
from vtimer.events import EventHandler, subscribe
from vtimer.menus import MENU_SELECTION_EVENT


def wait_for_selection():
    handler = EventHandler(MENU_SELECTION_EVENT)
    while not handler.has_event():
        vtimer.keypad.update()
