import time
import math
import collections

# Import libraries for Pimoroni Mechanical Keypad
from pmk.platform.keybow2040 import Keybow2040
from pmk import PMK

keybow2040 = Keybow2040()
keypad = PMK(keybow2040)

NOT_A_KEY_NUMBER = -2
NOT_AN_OPTION_VALUE = -1

rotated_key_num = [0, 4, 8,  12,
                   1, 5, 9,  13,
                   2, 6, 10, 14,
                   3, 7, 11, 15]

key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "cyan": (0, 255, 255),
               "orange": (255, 165, 0),
               "none": (0, 0, 0)}

all_keys = frozenset(range(0, 16))


def main_sequence():
    while True:
        minutes_menu = Menu()
        minutes_menu.options = [MenuOption(0, "red", 5),
                                MenuOption(1, "green", 10),
                                MenuOption(2, "blue", 15)]

        available_options_view = AvailableOptionsView(minutes_menu.options)
        available_options_view.display()

        minutes_menu.wait_for_selection()

        view = MinutesSelectedView(minutes_menu)
        view.display()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()

        multiplier_menu = Menu()
        multiplier_menu.options = [MenuOption(key_num, "cyan", key_num + 1)
                                   for key_num in range(0, 16)]

        available_options_view = AvailableOptionsView(multiplier_menu.options)
        available_options_view.display()

        multiplier_menu.wait_for_selection()

        view = MultiplierSelectedView(multiplier_menu)
        view.display()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()

        timer = Timer(minutes_menu.selected_option.value,
                      multiplier_menu.selected_option.value)

        timer.start()

        print(timer)

        monitor = TimerMonitor(minutes_menu, multiplier_menu, timer)
        monitor.wait_for_timer()

        if timer.is_cancelled():
            continue

        set_all_keys_colour("orange")
        wait = KeypressWait()
        wait.wait()


class Menu:
    def __init__(self):
        self._options = dict()
        self._selection_handler = MenuSelectionHandler()
        self.selected_option = MenuOption(key_num=NOT_A_KEY_NUMBER, colour="none", value=NOT_AN_OPTION_VALUE)

    @property
    def options(self):
        return self._options.values()

    @options.setter
    def options(self, option_list):
        for option in option_list:
            self._add_option(option)
        self.fill_missing_options()

    def _add_option(self, option):
        self._options[option.key_num] = option

    @property
    def _unused_keys(self):
        options_keys = set(self._options.keys())
        return all_keys - options_keys

    @property
    def unselected_keys(self):
        return all_keys - {self.selected_option.key_num}

    def fill_missing_options(self):
        for key_num in self._unused_keys:
            not_an_option = MenuOption(key_num=key_num, colour="none", value=NOT_AN_OPTION_VALUE)
            self._add_option(not_an_option)

    def wait_for_selection(self):
        while True:
            keypad.update()
            key_num = self._selection_handler.selected_key_num
            if key_num in all_keys:
                option = self._options[key_num]
                if option.value is not NOT_AN_OPTION_VALUE:
                    self.selected_option = option
                    return


MenuOption = collections.namedtuple("MenuOption", ["key_num", "colour", "value"])


class MenuSelectionHandler:
    def __init__(self):
        self.selected_key_num = NOT_A_KEY_NUMBER
        self._enable_choice_on_keypress()

    def _enable_choice_on_keypress(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(choice_key):
                pressed_list = keypad.get_pressed()
                self._on_press_select(pressed_list)

    def _on_press_select(self, pressed_list):
        if len(pressed_list) == 1:
            pressed = pressed_list[0]
            self.selected_key_num = rotated_key_num[pressed]


class MinutesSelectedView:
    def __init__(self, menu):
        self._option = menu.selected_option
        self._unselected_keys = menu.unselected_keys

    def display(self):
        set_key_colour(self._option.key_num, self._option.colour)

        for key_num in self._unselected_keys:
            set_key_colour(key_num, "none")


class MultiplierSelectedView:
    def __init__(self, menu):
        self._menu = menu

    def display(self):
        for key_num in self._keys_equal_to_or_less_than():
            set_key_colour(key_num, "cyan")

        for key_num in self._keys_greater_than():
            set_key_colour(key_num, "none")

    def _keys_equal_to_or_less_than(self):
        key_le = set()

        for option in self._menu.options:
            if option.key_num <= self._menu.selected_option.key_num:
                key_le.add(option.key_num)
        return key_le

    def _keys_greater_than(self):
        return all_keys - self._keys_equal_to_or_less_than()


class AvailableOptionsView:
    def __init__(self, options):
        self._options = options

    def display(self):
        for option in self._options:
            set_key_colour(option.key_num, option.colour)


class TimerMonitor:
    def __init__(self, minutes_menu, multiplier_menu, timer):
        self.minutes_menu = minutes_menu
        self.multiplier_menu = multiplier_menu
        self.timer = timer

        self._cancel_handler = CancelHandler()
        self._next_view_handler = NextViewHandler()

        self._views = [
            SimpleIndicatorView(key_num=0, colour="orange"),
            MinutesSelectedView(minutes_menu),
            MultiplierSelectedView(multiplier_menu),
            ProgressView(timer)
        ]

    def wait_for_timer(self):
        for view in cycle(self._views):
            set_all_keys_colour("none")
            while not self._next_view_handler.pressed:
                if self.timer.is_complete():
                    return

                if self._cancel_handler.cancelled:
                    self.timer.cancel()
                    return

                view.display()
                keypad.update()


# A simple implementation of itertools.cycle()
def cycle(iterable):
    while True:
        for element in iterable:
            yield element


class CancelHandler:
    def __init__(self):
        self.cancelled = False
        self.enable_on_hold()

    def enable_on_hold(self):
        for key in keypad.keys:
            @keypad.on_hold(key)
            def handler(key):
                self.cancelled = True


class NextViewHandler:
    def __init__(self):
        self._pressed = False
        self._enable_on_press()

    def _enable_on_press(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(key):
                self._pressed = True

    @property
    def pressed(self):
        is_pressed = self._pressed
        if self._pressed:
            self._pressed = False
        return is_pressed


class SimpleIndicatorView:
    def __init__(self, key_num, colour):
        self._key_num = key_num
        self._colour = colour

    def display(self):
        set_key_colour(self._key_num, self._colour)


class ProgressView:
    def __init__(self, timer):
        self.timer = timer

    def display(self):
        fraction = self.timer.fraction_remaining()
        keys_to_be_lit = math.ceil(16 * fraction)
        green_keys = set(range(0, keys_to_be_lit))
        blue_keys = all_keys - green_keys

        for key_num in green_keys:
            set_key_colour(key_num, "green")

        for key_num in blue_keys:
            set_key_colour(key_num, "blue")


class Timer:
    def __init__(self, minutes, multiplier):
        self.started = False
        self._cancelled = False
        self._minutes = minutes
        self._multiplier = multiplier
        self._start_time_seconds = 0

    def get_minutes(self):
        return self._minutes

    def get_multiplier(self):
        return self._multiplier

    def start(self):
        self.started = True
        self._start_time_seconds = time.monotonic()

    def cancel(self):
        self._cancelled = True

    def is_cancelled(self):
        return self._cancelled

    def is_complete(self):
        return self.total_seconds() <= self.seconds_passed()

    def total_minutes(self):
        return self._multiplier * self._minutes

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

    def __str__(self):
        return f"Timer set: {self._minutes} x {self._multiplier} = {self.total_minutes()} minutes"


class KeypressWait:
    def __init__(self):
        self._pressed = False

        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(key):
                self._pressed = True

    def wait(self):
        while not self._pressed:
            keypad.update()


class Pause:
    def __init__(self, seconds):
        self._seconds_to_pause_for = seconds
        self._start = time.monotonic()

    def complete(self):
        now = time.monotonic()
        paused_for = now - self._start
        return paused_for > self._seconds_to_pause_for

    def wait_until_complete(self):
        while not self.complete():
            keypad.update()


def set_key_colour(key_num, colour):
    key_num = rotated_key_num.index(key_num)
    keypad.keys[key_num].set_led(*key_colours[colour])


def set_all_keys_colour(colour):
    keypad.set_all(*key_colours[colour])


main_sequence()
