import vtimer
import vtimer.events


def wait_for_selection(menu):
    selection_made = False

    def handle(event):
        nonlocal selection_made
        selection_made = True

    vtimer.events.subscribe("menu_selection_made", handle)

    while not selection_made:
        vtimer.keypad.update()
