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
    def keypad_index_to_rotated(actual):
        return RotatedKeys._pmk_to_rotated_map[actual]

    @staticmethod
    def rotated_to_keypad_index(rotated):
        actual_list = list(RotatedKeys._pmk_to_rotated_map.keys())
        rotated_list = list(RotatedKeys._pmk_to_rotated_map.values())
        index = rotated_list.index(rotated)
        return actual_list[index]


class MenuMaker:
    def __init__(self):
        pass

    def make_minutes_menu(self):
        menu = Menu()

        five_selector = IntegerSelector(key_number=0,
                                        integer_value=5)

        ten_selector = IntegerSelector(key_number=4,
                                       integer_value=10)

        fifteen_selector = IntegerSelector(key_number=8,
                                           integer_value=15)

        five_selector.set_colour("red")
        ten_selector.set_colour("green")
        fifteen_selector.set_colour("blue")

        menu.add_selector(five_selector)
        menu.add_selector(ten_selector)
        menu.add_selector(fifteen_selector)

        menu.light_all_selectors()

        return menu

    def make_multiplier_menu(self):
        menu = Menu()

        for keypad_index in range(0, 16):
            rotated_key_number = RotatedKeys.keypad_index_to_rotated(keypad_index)
            integer_value = rotated_key_number + 1

            selector = IntegerSelector(key_number=keypad_index,
                                       integer_value=integer_value)
            selector.set_colour("cyan")
            menu.add_selector(selector)

        return menu


class Menu:
    def __init__(self):
        self._selectors = []

    def add_selector(self, selector):
        self._selectors.append(selector)
        selector.enable_keypress()

    def get_selected_value(self):
        for selector in self._selectors:
            if selector.selected:
                return selector.integer_value
        return None

    def reset_menu(self):
        for selector in self._selectors:
            selector.selected = False

    def get_selected_key(self):
        for selector in self._selectors:
            if selector.selected:
                return selector
        return None

    def light_keys_up_to_selected_value(self):
        selected_key = self.get_selected_key()
        for selector in self._selectors:
            if selector.integer_value <= selected_key.integer_value:
                selector.led_on()
            else:
                selector.led_off()

    def light_all_selectors(self):
        for selector in self._selectors:
            selector.led_on()


class IntegerSelector:
    def __init__(self, key_number, integer_value):
        self.key_number = key_number
        self.integer_value = integer_value
        self._key = pmk.keys[key_number]
        self.selected = False
        self._on_colour = "none"
        self._off_colour = "none"

    def set_colour(self, colour):
        self._on_colour = colour

    def get_rotated_key_number(self):
        return RotatedKeys.keypad_index_to_rotated(self.key_number)

    def enable_keypress(self):
        @pmk.on_press(self._key)
        def select(choice_key):
            self.selected = True

    def led_on(self):
        self._key.set_led(*key_colours[self._on_colour])

    def led_off(self):
        self._key.set_led(*key_colours[self._off_colour])


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
    maker = MenuMaker()
    menu = maker.make_minutes_menu()

    monitor = ValueChangeMonitor()
    while True:
        minutes = menu.get_selected_value()
        monitor.update_value(minutes)
        if monitor.value_has_changed():
            print(f"Minutes set to: {minutes}")
            menu.reset_menu()
        pmk.update()


def test_multiplier_menu():
    maker = MenuMaker()
    menu = maker.make_multiplier_menu()

    monitor = ValueChangeMonitor()

    while True:
        multiplier = menu.get_selected_value()
        monitor.update_value(multiplier)
        if monitor.value_has_changed():
            menu.light_keys_up_to_selected_value()
            print(f"Multiplier set to: {multiplier}")
            menu.reset_menu()
        pmk.update()


def test_integer_selector():
    selector = IntegerSelector(key_number=0, integer_value=1)
    selector.set_colour("orange")
    selector.enable_keypress()
    selector.led_on()

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
            rotated_number = RotatedKeys.keypad_index_to_rotated(pmk_number)
            if turn_on:
                pmk.keys[rotated_number].set_led(0, 255, 0)
            else:
                pmk.keys[rotated_number].set_led(0, 0, 0)
            time.sleep(0.2)
            pmk.update()

        turn_on = not turn_on


# test_minutes_menu()
test_multiplier_menu()
# test_integer_selector()
# test_rotated_keys()
