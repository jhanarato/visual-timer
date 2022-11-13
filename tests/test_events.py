import pytest

import vtimer.events
from vtimer import events
from vtimer.events import EventHandler


@pytest.fixture
def reset_subscriptions():
    events.subscribers.clear()


def test_subscribe(reset_subscriptions):
    handler = EventHandler()

    events.subscribe("test_event", handler)
    events.post_event("test_event", None)


def test_post_event(reset_subscriptions):
    handler = EventHandler()

    events.subscribe("test_event", handler)
    events.post_event("test_event", 123)

    assert handler.event == 123


def test_subscribe_twice(reset_subscriptions):
    handler_one = EventHandler()
    handler_two = EventHandler()

    events.subscribe("test_event", handler_one)
    events.subscribe("test_event", handler_two)
    events.post_event("test_event", None)
