# This code is adapted from Arjan Eggles' better python repository
# https://github.com/ArjanCodes/betterpython
# Copyright 2021

subscribers = dict()


def subscribe(event_type:str, fn):
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)


def post_event(event_type: str, data):
    if event_type not in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(data)


class EventHandler:
    def __init__(self):
        self._event = None

    def __call__(self, event):
        self._event = event

    @property
    def event(self):
        if self._event is None:
            raise Exception("No event has arrived")

        return self._event

    def has_event(self):
        return self._event is not None
