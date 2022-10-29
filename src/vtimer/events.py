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


class Observer:
    def __init__(self, event_type):
        subscribe(event_type, self.receive)
        self.has_seen = False

    def receive(self, event):
        self.has_seen = True
