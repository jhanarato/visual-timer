from vtimer import events
from vtimer.util import partial


def test_subscribe():
    def handler():
        pass

    events.subscribe("test_event", handler)


def test_post_event():
    class Handler:
        def __init__(self):
            self.value = 0

        def handle(self, value):
            self.value = value

    handler = Handler()

    events.subscribe("test_event", handler.handle)
    events.post_event("test_event", 123)

    assert handler.value == 123


def test_with_partial():
    class ValueHolder:
        def __init__(self):
            self.value = 0

    def handler(value_holder, value):
        value_holder.value = value

    value_holder = ValueHolder()
    value_holder.value = 50

    handler_with_holder = partial(handler, value_holder)

    events.subscribe("test_event", handler_with_holder)
    events.post_event("test_event", 100)

    assert value_holder.value == 100


def test_keypress_logger():

    assert False