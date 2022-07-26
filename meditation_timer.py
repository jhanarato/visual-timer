import time
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
               "orange": (255, 165, 0),
               "none": (0, 0, 0)}

rotated_keys = {
    0: 0,  1: 4,  2: 8,   3: 12,
    4: 1,  5: 5,  6: 9,   7: 13,
    8: 2,  9: 6,  10: 10, 11: 14,
    12: 3, 13: 7, 14: 11, 15: 15
}


class MinutesMenu:
    def __init__(self):
        self._selectors = []

        five_selector = IntegerSelector(key_number=0, integer_value=5)
        five_selector.set_colour("red")
        self._selectors.append(five_selector)

        ten_selector = IntegerSelector(key_number=4, integer_value=10)
        ten_selector.set_colour("green")
        self._selectors.append(ten_selector)

        fifteen_selector = IntegerSelector(key_number=8, integer_value=15)
        fifteen_selector.set_colour("blue")
        self._selectors.append(fifteen_selector)

        self._enable_all_selectors()

    def _enable_all_selectors(self):
        for selector in self._selectors:
            selector.enable()

    def get_minutes_selected(self):
        for selector in self._selectors:
            if selector.selected:
                return selector.integer_value
        return None

    def reset_menu(self):
        for selector in self._selectors:
            selector.selected = False


class MultiplierMenu:
    def __init__(self):
        self._selectors = []
        self._add_selectors()
        self._set_colour()
        self._enable_all_selectors()

    def _add_selectors(self):
        for pmk_number in range(0, 16):
            rotated_number = RotatedKeys.pmk_to_rotated(pmk_number)
            selector = IntegerSelector(key_number=pmk_number,
                                       integer_value=rotated_number + 1)
            self._selectors.append(selector)

    def _set_colour(self):
        # TODO Only keys up to the selected value should be lit.
        for selector in self._selectors:
            selector.set_colour("cyan")

    def _enable_all_selectors(self):
        for selector in self._selectors:
            selector.enable()

    def get_multiplier_selected(self):
        for selector in self._selectors:
            if selector.selected:
                return selector.integer_value
        return None

    def reset_menu(self):
        for selector in self._selectors:
            selector.selected = False

    def show_selection(self):
        selected_key_number = 0
        for selector in self._selectors:
            if selector.selected:
                selected_key_number = selector.key_number
                break

        for selector in self._selectors:
            if selector.key_number >= selected_key_number:
                selector.set_colour("cyan")
            else:
                selector.set_colour("none")


class RotatedKeys:
    _pmk_to_rotated_map = {
        0: 0, 1: 4, 2: 8, 3: 12,
        4: 1, 5: 5, 6: 9, 7: 13,
        8: 2, 9: 6, 10: 10, 11: 14,
        12: 3, 13: 7, 14: 11, 15: 15
    }

    def __init__(self):
        pass

    @staticmethod
    def pmk_to_rotated(actual):
        return RotatedKeys._pmk_to_rotated_map[actual]

    @staticmethod
    def rotated_to_pmk(rotated):
        actual_list = list(RotatedKeys._pmk_to_rotated_map.keys())
        rotated_list = list(RotatedKeys._pmk_to_rotated_map.values())
        index = rotated_list.index(rotated)
        return actual_list[index]


class IntegerSelector:
    def __init__(self, key_number, integer_value):
        self.key_number = key_number
        self.integer_value = integer_value
        self._key = pmk.keys[key_number]
        self.selected = False

    def set_colour(self, colour):
        self._key.set_led(*key_colours[colour])

    def enable(self):
        @pmk.on_press(self._key)
        def select(choice_key):
            self.selected = True


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


def test_multiplier_menu():
    menu = MultiplierMenu()
    monitor = ValueChangeMonitor()

    while True:
        multiplier = menu.get_multiplier_selected()
        monitor.update_value(multiplier)
        if monitor.value_has_changed():
            # menu.show_selection()
            print(f"Multiplier set to: {multiplier}")
            menu.reset_menu()
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


def test_rotated_keys():
    print("Test 1")
    turn_on = True
    while True:
        for pmk_number in range(0, 16):
            rotated_number = RotatedKeys.pmk_to_rotated(pmk_number)
            if turn_on:
                pmk.keys[rotated_number].set_led(0, 255, 0)
            else:
                pmk.keys[rotated_number].set_led(0, 0, 0)
            time.sleep(0.2)
            pmk.update()

        turn_on = not turn_on


# test_integer_selector()
# test_minutes_menu()
test_multiplier_menu()
# test_rotated_keys()
