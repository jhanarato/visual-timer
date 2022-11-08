class Handler:
    def __init__(self):
        self._event = None

    def __call__(self, event):
        self._event = event

    @property
    def event(self):
        if self._event is None:
            raise Exception("No event has arrived")

        return self._event
