import pytest
from pydispatch import dispatcher


class EventSender:
    def __init__(self, value):
        self.value = value


def handle_change_value(sender):
    sender.value = 321


def test_event_handled():
    dispatcher.connect(handle_change_value, signal='change-value', sender=dispatcher.Any)

    sender = EventSender(123)
    assert sender.value == 123

    dispatcher.send(signal='change-value', sender=sender)
    assert sender.value == 321

