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


class ValueChangeMonitor:
    def __init__(self):
        self._old_value = None
        self._changed = False

    def update_value(self, new_value):
        if new_value is not None:
            if self._old_value != new_value:
                self._old_value = new_value
                self._changed = True

    def value_has_changed(self):
        if self._changed:
            self._changed = False
            return True
        else:
            return False


def test_minutes_menu():
    minutes_menu = MinutesMenu()
    monitor = ValueChangeMonitor()
    while True:
        minutes = minutes_menu.get_minutes_selected()
        monitor.update_value(minutes)
        if monitor.value_has_changed():
            print(f"Minutes set to: {minutes}")
            minutes_menu.reset_menu()
        pmk.update()


test_minutes_menu()
