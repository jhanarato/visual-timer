import vtimer
import vtimer.events
import vtimer.menus


def wait_for_selection(menu):
    selection_made = False

    def handle(event):
        nonlocal selection_made
        selection_made = True

    vtimer.events.subscribe(vtimer.menus.MENU_SELECTION_EVENT, handle)

    while not selection_made:
        vtimer.keypad.update()
