import pytest

import vtimer.events
from vtimer import events
from vtimer.events import EventHandler, EventOverwriteException

TEST_EVENT = "test_event"

@pytest.fixture
def reset_subscriptions():
    events.subscribers.clear()


def test_subscribe(reset_subscriptions):
    handler = EventHandler(TEST_EVENT)
    events.post_event(TEST_EVENT, None)


def test_post_event(reset_subscriptions):
    handler = EventHandler(TEST_EVENT)
    events.post_event(TEST_EVENT, 123)

    assert handler.event == 123


def test_subscribe_twice(reset_subscriptions):
    handler_one = EventHandler(TEST_EVENT)
    handler_two = EventHandler(TEST_EVENT)
    events.post_event(TEST_EVENT, None)


def test_exception_on_event_overwrite(reset_subscriptions):
    handler = EventHandler(TEST_EVENT)
    events.post_event(TEST_EVENT, 123)
    with pytest.raises(EventOverwriteException):
        events.post_event(TEST_EVENT, 321)
