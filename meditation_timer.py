from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)

# Shortcuts for various switch LED colours
key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "cyan": (0, 255, 255),
               "orange": (255, 165, 0)}


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

    def __init__(self, key_number, minutes):
        self._key = pmk.keys[key_number]
        self.minutes = minutes
        self.selected = False

    def set_colour(self, colour):
        self._key.set_led(*key_colours[colour])

    def enable(self):
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

        five_selector = MinutesSelector(key_number=0, minutes=5)
        five_selector.set_colour("red")
        self._selectors.append(five_selector)

        ten_selector = MinutesSelector(key_number=4, minutes=10)
        ten_selector.set_colour("green")
        self._selectors.append(ten_selector)

        fifteen_selector = MinutesSelector(key_number=8, minutes=15)
        fifteen_selector.set_colour("blue")
        self._selectors.append(fifteen_selector)

        self._enable_all_selectors()

    def _enable_all_selectors(self):
        for selector in self._selectors:
            selector.enable()

    def get_minutes_selected(self):
        for selector in self._selectors:
            if selector.selected:
                return selector.minutes
        return None

    def reset_menu(self):
        for selector in self._selectors:
            selector.selected = False


class IntegerSelector:
    def __init__(self, key_number, integer_value):
        self._key = pmk.keys[key_number]
        self.integer_value = integer_value
        self.selected = False

    def set_colour(self, colour):
        self._key.set_led(*key_colours[colour])

    def enable(self):
        @pmk.on_press(self._key)
        def select(choice_key):
            self.selected = True


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


def test_integer_selector():
    selector = IntegerSelector(key_number=0, integer_value=1)
    selector.set_colour("orange")
    selector.enable()

    message_printed = False
    while True:
        if selector.selected and not message_printed:
            print(f"Integer {selector.integer_value} selected")
            message_printed = True
        pmk.update()


test_integer_selector()
# test_minutes_menu()
