import pytest

import vtimer.events
from vtimer import events
from vtimer.events import Handler


@pytest.fixture
def reset_subscriptions():
    events.subscribers.clear()


def test_subscribe(reset_subscriptions):
    handler = Handler()

    events.subscribe("test_event", handler)
    events.post_event("test_event", None)


def test_post_event(reset_subscriptions):
    handler = Handler()

    events.subscribe("test_event", handler)
    events.post_event("test_event", 123)

    assert handler.event == 123


def test_subscribe_twice(reset_subscriptions):
    handler_one = Handler()
    handler_two = Handler()

    events.subscribe("test_event", handler_one)
    events.subscribe("test_event", handler_two)
    events.post_event("test_event", None)


def test_event_observer(reset_subscriptions):
    observer = vtimer.events.Observer("test_event")
    vtimer.events.post_event("test_event", 123)
    assert observer.has_seen
