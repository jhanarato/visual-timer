import vtimer
from vtimer.events import EventHandler


def wait_for_event(event_type):
    handler = EventHandler(event_type)
    while not handler.has_event():
        vtimer.keypad.update()
