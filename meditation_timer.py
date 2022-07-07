from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)


class Timer:
    def __init__(self):
        self.is_set = False
        self.time_units = 0
        self.number_of_units = 0

    def start(self):
        minutes = self.time_units * self.number_of_units
        print(f"Timer set: {minutes} minutes")
        self.is_set = True

    def is_complete(self):
        # TODO Check if the time has elapsed.
        return self.is_set


class UnitsSelector:
    def __init__(self, key, timer_to_set, units, colour):
        self._key = key
        self._key.set_led(*colour)

        self._timer = timer_to_set
        self._units = units

        self._add_handler()

    def _add_handler(self):
        @pmk.on_press(self._key)
        def handler(unit_key):
            self._timer.time_units = self._units
            self._timer.start()


timer = Timer()

five_minute_selector = UnitsSelector(pmk.keys[0], timer, 5, (255, 0, 0))
ten_minute_selector = UnitsSelector(pmk.keys[4], timer, 10, (0, 255, 0))
fifteen_minute_selector = UnitsSelector(pmk.keys[8], timer, 15, (0, 0, 255))


# TODO User selects the number to multiply the units.
timer.number_of_units = 3

msg_shown = False
while True:
    # We only want to print the message once
    if not msg_shown and timer.is_complete():
        print("Time's up")
        msg_shown = True

    pmk.update()
