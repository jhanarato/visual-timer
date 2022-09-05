import time
import math
import collections

# Import libraries for Pimoroni Mechanical Keypad
from pmk.platform.keybow2040 import Keybow2040
from pmk import PMK

keybow2040 = Keybow2040()
keypad = PMK(keybow2040)

key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "cyan": (0, 255, 255),
               "orange": (255, 165, 0),
               "none": (0, 0, 0)}

all_keys = frozenset(range(0, 16))


class SequenceOfOperation:
    def __init__(self):
        pass

    def perform_sequence(self):
        # TODO: Clean up so we don't need to reset. Assuming reset does something.
        self.reset()

        minutes_menu = MinutesMenu()
        minutes = minutes_menu.get_users_choice()

        multiplier_menu = MultiplierMenu()
        multiplier = multiplier_menu.get_users_choice()

        timer = Timer(minutes, multiplier)
        timer.start()

        print(timer)

        monitor = TimerMonitor(minutes_menu, multiplier_menu, timer)
        monitor.monitor()

        if timer.is_cancelled():
            return

        self.show_complete_view()

        wait = KeypressWait()
        wait.wait()

    def show_complete_view(self):
        for key_num in all_keys:
            set_key_colour(key_num, "orange")
        keypad.update()

    def reset(self):
        for key in keypad.keys:
            set_key_colour(key.number, "none")

            @keypad.on_press(key)
            def handler(key):
                pass


class Menu:
    def __init__(self):
        self._options = dict()
        self.add_options()
        self._selection_handler = MenuSelectionHandler()

    def get_users_choice(self):
        self.light_all_option_keys()
        self._selection_handler.wait_for_selection()
        self.display_selection()
        pause = Pause(seconds=1.5)
        pause.wait_until_complete()
        return self.selected_option.value

    @property
    def options(self):
        return self._options.values()

    @property
    def selected_option(self):
        return self._options.get(self._selection_handler.selected_key_num)

    def add_option(self, option):
        self._options[option.key_num] = option

    def add_options(self):
        raise NotImplementedError

    def display_selection(self):
        raise NotImplementedError

    @property
    def unused_keys(self):
        options_keys = set(self._options.keys())
        return all_keys - options_keys

    @property
    def unselected_keys(self):
        return all_keys - {self.selected_option.key_num}

    def light_all_option_keys(self):
        for option in self.options:
            set_key_colour(option.key_num, option.colour)


MenuOption = collections.namedtuple("MenuOption", ["key_num", "colour", "value"])


class MenuSelectionHandler:
    NO_SELECTION = -1

    def __init__(self):
        self.selected_key_num = MenuSelectionHandler.NO_SELECTION
        self._enable_choice_on_keypress()

    def _enable_choice_on_keypress(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(choice_key):
                pressed_list = keypad.get_pressed()
                self._on_press_select(pressed_list)

    def _on_press_select(self, pressed_list):
        if self._selection_already_made():
            return

        if len(pressed_list) == 1:
            pressed = pressed_list[0]
            self.selected_key_num = rotate(pressed)

    def _selection_already_made(self):
        return self.selected_key_num is not MenuSelectionHandler.NO_SELECTION

    def wait_for_selection(self):
        while self.selected_key_num is MenuSelectionHandler.NO_SELECTION:
            keypad.update()


class MinutesMenu(Menu):
    def add_options(self):
        self.add_option(MenuOption(0, "red", 5))
        self.add_option(MenuOption(1, "green", 10))
        self.add_option(MenuOption(2, "blue", 15))

    def display_selection(self):
        set_key_colour(self.selected_option.key_num, self.selected_option.colour)

        for key_num in self.unselected_keys:
            set_key_colour(key_num, "none")


class MultiplierMenu(Menu):
    def add_options(self):
        for index in range(0, 16):
            multiplier_value = index + 1
            self.add_option(MenuOption(index, "cyan", multiplier_value))

    def display_selection(self):
        for key_num in self._keys_equal_to_or_less_than():
            set_key_colour(key_num, "cyan")

        for key_num in self._keys_greater_than():
            set_key_colour(key_num, "none")

    def _keys_equal_to_or_less_than(self):
        key_le = set()

        for option in self.options:
            if option.key_num <= self.selected_option.key_num:
                key_le.add(option.key_num)
        return key_le

    def _keys_greater_than(self):
        return all_keys - self._keys_equal_to_or_less_than()


class TimerMonitor:
    def __init__(self, minutes_menu, multiplier_menu, timer):
        self.minutes_menu = minutes_menu
        self.multiplier_menu = multiplier_menu
        self.timer = timer

        self.modes = MonitoringViewCycle()
        self.enable_next_view_on_keypress()
        self.enable_cancel_timer_on_keyhold()

    # TODO move keypress handling to new class
    def enable_next_view_on_keypress(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(key):
                self.modes.next()

    def enable_cancel_timer_on_keyhold(self):
        for key in keypad.keys:
            @keypad.on_hold(key)
            def handler(key):
                self.timer.cancel()

    def show_current_view(self):
        mode = self.modes.current()

        if mode == MonitoringViewCycle.ON_INDICATOR:
            self.show_indicator_view()
        if mode == MonitoringViewCycle.MINUTES:
            self.minutes_menu.display_selection()
        if mode == MonitoringViewCycle.MULTIPLIER:
            self.multiplier_menu.display_selection()
        if mode == MonitoringViewCycle.PROGRESS:
            self.show_progress_view()

    def show_indicator_view(self):
        indicator_key = 0
        selected = {indicator_key}
        not_selected = all_keys - selected

        for key_num in selected:
            set_key_colour(key_num, "orange")

        for key_num in not_selected:
            set_key_colour(key_num, "none")

    # TODO move to new class
    def show_progress_view(self):
        fraction = self.timer.fraction_remaining()
        keys_to_be_lit = math.ceil(16 * fraction)
        green_keys = set(range(0, keys_to_be_lit))
        blue_keys = all_keys - green_keys

        for key_num in green_keys:
            set_key_colour(key_num, "green")

        for key_num in blue_keys:
            set_key_colour(key_num, "blue")

    def monitor(self):
        while True:
            if self.timer.is_complete():
                return
            if self.timer.is_cancelled():
                return
            self.show_current_view()
            keypad.update()


class MonitoringViewCycle:
    ON_INDICATOR = "showing is on"
    MINUTES = "showing minutes"
    MULTIPLIER = "showing multiplier"
    PROGRESS = "showing progress"

    def __init__(self):
        self.modes = [MonitoringViewCycle.ON_INDICATOR,
                      MonitoringViewCycle.MINUTES,
                      MonitoringViewCycle.MULTIPLIER,
                      MonitoringViewCycle.PROGRESS]

        self.mode_index = 0

    def next(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes)

    def current(self):
        return self.modes[self.mode_index]


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


normal_to_rotated = {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
    4: 1,
    5: 5,
    6: 9,
    7: 13,
    8: 2,
    9: 6,
    10: 10,
    11: 14,
    12: 3,
    13: 7,
    14: 11,
    15: 15
}


def invert_dictionary(d):
    return {v: k for k, v in d.items()}


def rotate(key_num):
    return normal_to_rotated[key_num]


def undo_rotate(key_num):
    return invert_dictionary(normal_to_rotated)[key_num]


def set_key_colour(key_num, colour):
    key_num = undo_rotate(key_num)
    keypad.keys[key_num].set_led(*key_colours[colour])


# Run the application
sequence = SequenceOfOperation()

while True:
    sequence.perform_sequence()
