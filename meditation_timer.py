from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

class Hardware:
    _pmk = None

    @staticmethod
    def set_hardware(pmk):
        Hardware._pmk = pmk

    @staticmethod
    def get_hardware():
        if Hardware._pmk is None:
            raise ValueError("Hardware not initialised before use.")
        return Hardware._pmk

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

        five = IntegerSelector(rotated_key_index=0, integer_value=5)
        ten = IntegerSelector(rotated_key_index=1, integer_value=10)
        fifteen = IntegerSelector(rotated_key_index=2, integer_value=15)

        five.set_colour("red")
        ten.set_colour("green")
        fifteen.set_colour("blue")

        menu.add_selector(five)
        menu.add_selector(ten)
        menu.add_selector(fifteen)

        menu.light_all_selectors()

        return menu

    def make_multiplier_menu(self):
        menu = Menu()

        for index in range(0, 16):
            selector = IntegerSelector(rotated_key_index=index,
                                       integer_value=index + 1)

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
    def __init__(self, rotated_key_index, integer_value):
        self.key_index = RotatedKeys.rotated_to_keypad_index(rotated_key_index)
        self.integer_value = integer_value
        self._key = Hardware.get_hardware().keys[self.key_index]
        self.selected = False
        self._on_colour = "none"
        self._off_colour = "none"

    def set_colour(self, colour):
        self._on_colour = colour

    def get_rotated_key_number(self):
        return RotatedKeys.keypad_index_to_rotated(self.key_index)

    def enable_keypress(self):
        hardware = Hardware.get_hardware()

        @hardware.on_press(self._key)
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
