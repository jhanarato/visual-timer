from vtimer import events


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
