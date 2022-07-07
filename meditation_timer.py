from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)


class Timer:
    def __init__(self):
        self.is_set = False
        self.base_minutes = 0
        self.multiplier = 0

    def start(self):
        minutes = self.base_minutes * self.multiplier
        print(f"Timer set: {minutes} minutes")
        self.is_set = True

    def is_complete(self):
        # TODO Check if the time has elapsed.
        return self.is_set


class BaseMinutesSelector:
    def __init__(self, key, timer_to_set, minutes, colour):
        self._key = key
        self._key.set_led(*colour)

        self._timer = timer_to_set
        self._minutes = minutes

        self._add_handler()

    def _add_handler(self):
        @pmk.on_press(self._key)
        def handler(unit_key):
            self._timer.base_minutes = self._minutes
            self._timer.start()


timer = Timer()

five_minute_selector = BaseMinutesSelector(pmk.keys[0], timer, 5, (255, 0, 0))
ten_minute_selector = BaseMinutesSelector(pmk.keys[4], timer, 10, (0, 255, 0))
fifteen_minute_selector = BaseMinutesSelector(pmk.keys[8], timer, 15, (0, 0, 255))


# TODO User selects the number to multiply the units.
timer.multiplier = 3

msg_shown = False
while True:
    # We only want to print the message once
    if not msg_shown and timer.is_complete():
        print("Time's up")
        msg_shown = True

    pmk.update()
