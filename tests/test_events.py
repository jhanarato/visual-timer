import pytest

from vtimer import events
from vtimer.util import partial


@pytest.fixture
def reset_subscriptions():
    events.subscribers.clear()


def test_subscribe(reset_subscriptions):
    def handler(data):
        pass

    events.subscribe("test_event", handler)
    events.post_event("test_event", None)


def test_post_event(reset_subscriptions):
    class Handler:
        def __init__(self):
            self.value = 0

        def handle(self, value):
            self.value = value

    handler = Handler()

    events.subscribe("test_event", handler.handle)
    events.post_event("test_event", 123)

    assert handler.value == 123


def test_with_partial(reset_subscriptions):
    class ValueHolder:
        def __init__(self):
            self.value = 0

    def handler(holder, value):
        holder.value = value

    value_holder = ValueHolder()
    value_holder.value = 50

    handler_with_holder = partial(handler, value_holder)

    events.subscribe("test_event", handler_with_holder)
    events.post_event("test_event", 100)

    assert value_holder.value == 100


def test_subscribe_twice(reset_subscriptions):
    def handler_one(data):
        pass

    def handler_two(data):
        pass

    events.subscribe("test_event", handler_one)
    events.subscribe("test_event", handler_two)
    events.post_event("test_event", None)


def test_keypress_logger(reset_subscriptions):

    assert False