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

        self._enable_selection()

    def _enable_selection(self):
        @pmk.on_press(self._key)
        def select(choice_key):
            self.selected = True


class MinutesMenu:
    """
    A group of keys allowing the selection of the number of minutes
    to be multiplied.
    """

    def __init__(self):
        self._selectors = []
        self._selectors.append(MinutesSelector(pmk.keys[0], 5, "red"))
        self._selectors.append(MinutesSelector(pmk.keys[4], 10, "green"))
        self._selectors.append(MinutesSelector(pmk.keys[8], 15, "blue"))

    def get_minutes_selected(self):
        for selector in self._selectors:
            if selector.selected:
                return selector.minutes
        return None

    def reset_menu(self):
        for selector in self._selectors:
            selector.selected = False


class MultiplierSelector:
    """
    Setup keypress handlers to choose how many times to multiply
    the base number of minutes in order to select the total time.
    """

    def __init__(self):
        pass


class ValueChangedLogger:
    def __init__(self, message_prefix):
        self._old_value = None
        self._message_prefix = message_prefix

    def update_value(self, new_value):
        if new_value is not None:
            if self._old_value != new_value:
                print(f"{self._message_prefix}: {new_value}")
                self._old_value = new_value


def test_logger():
    logger = ValueChangedLogger("Test Logger")
    logger.update_value(1)  # Print "Test Logger: 1"
    logger.update_value(2)  # Print "Test Logger: 2"
    logger.update_value(2)  # No output
    logger.update_value(3)  # Print "Test Logger: 3"


def test_minutes_menu():
    minutes_menu = MinutesMenu()
    logger = ValueChangedLogger("Minutes")
    while True:
        minutes = minutes_menu.get_minutes_selected()
        logger.update_value(minutes)
        pmk.update()


def run_forever():
    pass


#test_logger()
test_minutes_menu()
# run_forever()
