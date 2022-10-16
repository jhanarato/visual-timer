import time


class Timer:
    def __init__(self):
        self.minutes = 0
        self.multiplier = 0
        self.started = False
        self.cancelled = False
        self._start_time_seconds = 0

    def start(self):
        self.started = True
        self.cancelled = False
        self._start_time_seconds = time.monotonic()
        print(f"Timer set: {self.minutes} x {self.multiplier} = {self.total_minutes()} minutes")

    @property
    def complete(self):
        return self.total_seconds() <= self.seconds_passed()

    @property
    def running(self):
        return self.started and not self.complete and not self.cancelled

    def reset(self):
        self.minutes = 0
        self.multiplier = 0
        self.started = False
        self.cancelled = False
        self._start_time_seconds = 0

    def total_minutes(self):
        return self.multiplier * self.minutes

    def total_seconds(self):
        return self.total_minutes() * 60

    def seconds_passed(self):
        return time.monotonic() - self._start_time_seconds

    def minutes_passed(self):
        return math.floor(self.seconds_passed() / 60)

    def seconds_remaining(self):
        return self.total_seconds() - self.seconds_passed()

    def minutes_remaining(self):
        return self.total_minutes() - self.minutes_passed()

    def fraction_remaining(self):
        return self.seconds_remaining() / self.total_seconds()
