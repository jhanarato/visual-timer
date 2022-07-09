from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)

# Shortcuts for various switch LED colours
key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255)}


class Timer:
    """
    Once we know the number of minutes assigned per key and
    the number of keys selected, multiply the two and track
    when the total number of minutes has passed.
    """
    def __init__(self):
        self.started = False
        self.minutes = 0
        self.multiplier = 0

    def start(self):
        minutes = self.minutes * self.multiplier
        print(f"Timer started: {minutes} minutes")
        self.started = True

    def is_complete(self):
        # TODO Check if the time has elapsed.
        return self.started


class MinutesSelector:
    """
    Assign a handler to a single key to choose the number
    of minutes to be multiplied.
    """
    def __init__(self, key, minutes, colour):
        self._key = key
        self._key.set_led(*key_colours[colour])
        self.minutes = minutes
        self.selected = False

        self._add_handler()

    def _add_handler(self):
        @pmk.on_press(self._key)
        def handler(unit_key):
            self.selected = True


class MultiplierSelector:
    """
    Setup keypress handlers to choose how many times to multiply
    the base number of minutes in order to select the total time.
    """
    def __init__(self):
        pass


# There is a single timer
timer = Timer()

# Allow a choice of 5, 10 or 15 minutes. Red, green and blue respectively.
minute_selectors = [
    MinutesSelector(pmk.keys[0], 5, "red"),
    MinutesSelector(pmk.keys[4], 10, "green"),
    MinutesSelector(pmk.keys[8], 15, "blue")
]

# TODO User selects the number to multiply the units.
timer.multiplier = 3

msg_shown = False

while True:
    for minute_selector in minute_selectors:
        if minute_selector.selected:
            timer.minutes = minute_selector.minutes
            if not timer.started:
                timer.start()

    # We only want to print the message once
    if not msg_shown and timer.is_complete():
        print("Time's up")
        msg_shown = True

    pmk.update()
