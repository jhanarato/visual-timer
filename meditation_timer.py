import time
import math
import collections

from pmk.platform.keybow2040 import Keybow2040
from pmk import PMK

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
        Hardware.reset()

        minutes_menu = MinutesMenu()
        minutes = minutes_menu.get_users_choice()

        multiplier_menu = MultiplierMenu()
        multiplier = multiplier_menu.get_users_choice()

        timer = Timer(minutes, multiplier)
        timer.start()

        print(timer)

        self.monitor_timer(timer)

        if timer.is_cancelled():
            return

        self.show_complete_view()

        wait = KeypressWait()
        wait.wait()

    def monitor_timer(self, timer):
        monitor = TimerMonitor(timer)
        while True:
            if timer.is_complete():
                return
            if timer.is_cancelled():
                return
            monitor.show_current_view()
            Hardware.update()

    def show_complete_view(self):
        for key_num in all_keys:
            set_key_colour(key_num, "orange")
        Hardware.update()


class Menu:
    def __init__(self):
        self._options = dict()
        self.add_options()
        self._selection_handler = MenuSelectionHandler()

    def get_users_choice(self):
        self.light_all_option_keys()
        self.wait_for_selection()
        self.display_selection()
        pause = Pause(seconds=1.5)
        pause.wait_until_complete()
        return self.selected_option.value

    def wait_for_selection(self):
        while self._selection_handler.selected_option is None:
            Hardware.update()

    @property
    def options(self):
        return self._options.values()

    @property
    def selected_option(self):
        return self._options[self._selection_handler.selected_option]

    @selected_option.setter
    def selected_option(self, key_num):
        if key_num in self._options:
            self._selection_handler.selected_option = self._options.get(key_num)

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
    def __init__(self):
        self.selected_option = None
        self._enable_choice_on_keypress()

    def _enable_choice_on_keypress(self):
        hardware = Hardware.get_hardware()

        for key in hardware.keys:
            @hardware.on_press(key)
            def handler(choice_key):
                pressed_list = hardware.get_pressed()
                self._on_press_select(pressed_list)

    def _on_press_select(self, pressed_list):
        if len(pressed_list) != 1:
            return

        pressed = pressed_list[0]
        rotator = KeyRotator()
        rotated = rotator.to_rotated_orientation(pressed)
        self.selected_option = rotated


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
        # TODO no need to pass a member as a parameter
        for key_num in self._keys_equal_to_or_less_than(self.selected_option.key_num):
            set_key_colour(key_num, "cyan")

        for key_num in self._keys_greater_than(self.selected_option.key_num):
            set_key_colour(key_num, "none")

    def _keys_equal_to_or_less_than(self, key_num):
        return {option.key_num for option in self.options if option.key_num <= key_num}

    def _keys_greater_than(self, key_num):
        return all_keys - self._keys_equal_to_or_less_than(key_num)


class TimerMonitor:
    def __init__(self, timer):
        self._timer = timer
        self.modes = MonitoringViewCycle()
        self.enable_next_view_on_keypress()
        self.enable_cancel_timer_on_keyhold()

    def enable_next_view_on_keypress(self):
        hardware = Hardware.get_hardware()
        for key in hardware.keys:
            @hardware.on_press(key)
            def handler(key):
                self.modes.next()

    def enable_cancel_timer_on_keyhold(self):
        hardware = Hardware.get_hardware()
        for key in hardware.keys:
            @hardware.on_hold(key)
            def handler(key):
                self._timer.cancel()

    def show_current_view(self):
        mode = self.modes.current()

        if mode == MonitoringViewCycle.ON_INDICATOR:
            self.show_indicator_view()
        if mode == MonitoringViewCycle.MINUTES:
            self.show_minutes_view()
        if mode == MonitoringViewCycle.MULTIPLIER:
            self.show_multiplier_view()
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

    def show_minutes_view(self):
        minutes = self._timer.get_minutes()
        selected = set()

        if minutes == 5:
            selected.add(0)
            set_key_colour(0, "red")
        if minutes == 10:
            selected.add(1)
            set_key_colour(1, "green")
        if minutes == 15:
            selected.add(2)
            set_key_colour(2, "blue")

        not_selected = all_keys - selected

        for key_num in not_selected:
            set_key_colour(key_num, "none")

    def show_multiplier_view(self):
        multiplier = self._timer.get_multiplier()
        selected = set(range(0, multiplier))
        not_selected = all_keys - selected

        for key_num in selected:
            set_key_colour(key_num, "cyan")

        for key_num in not_selected:
            set_key_colour(key_num, "none")

    def show_progress_view(self):
        fraction = self._timer.fraction_remaining()
        keys_to_be_lit = math.ceil(16 * fraction)
        green_keys = set(range(0, keys_to_be_lit))
        blue_keys = all_keys - green_keys

        for key_num in green_keys:
            set_key_colour(key_num, "green")

        for key_num in blue_keys:
            set_key_colour(key_num, "blue")


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


class Hardware:
    _pmk = None
    rotator = None

    @staticmethod
    def set_hardware(pmk):
        Hardware._pmk = pmk
        Hardware.rotator = KeyRotator()

    @staticmethod
    def get_hardware():
        if Hardware._pmk is None:
            raise ValueError("Hardware not initialised before use.")
        return Hardware._pmk

    @staticmethod
    def reset():
        hardware = Hardware._pmk
        for key in hardware.keys:
            key.set_led(*key_colours["none"])

            @hardware.on_press(key)
            def handler(key):
                pass

    @staticmethod
    def update():
        hardware = Hardware._pmk
        hardware.update()

    @staticmethod
    def get_key(index):
        return Hardware._pmk.keys[index]

    @staticmethod
    def get_rotated_key(index):
        rotated_index = Hardware.rotator.to_device_orientation(index)
        return Hardware._pmk.keys[rotated_index]

    @staticmethod
    def set_all_colour(colour):
        Hardware._pmk.set_all(*key_colours[colour])

    @staticmethod
    def any_key_pressed():
        Hardware.update()
        return Hardware._pmk.any_pressed()


class KeypressWait:
    def __init__(self):
        self._pressed = False

        hardware = Hardware.get_hardware()

        for key in hardware.keys:
            @hardware.on_press(key)
            def handler(key):
                self._pressed = True

    def wait(self):
        while not self._pressed:
            Hardware.update()


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
            Hardware.update()


class KeyRotator:
    def __init__(self):
        self._device_to_rotated = {
            0: 0, 1: 4, 2: 8, 3: 12,
            4: 1, 5: 5, 6: 9, 7: 13,
            8: 2, 9: 6, 10: 10, 11: 14,
            12: 3, 13: 7, 14: 11, 15: 15
        }

    def to_rotated_orientation(self, device_key_number):
        return self._device_to_rotated[device_key_number]

    def to_device_orientation(self, rotated_key_number):
        actual_list = list(self._device_to_rotated.keys())
        rotated_list = list(self._device_to_rotated.values())
        index = rotated_list.index(rotated_key_number)
        return actual_list[index]


def set_key_colour(key_num, colour):
    key_num = Hardware.rotator.to_device_orientation(key_num)
    pmk.keys[key_num].set_led(*key_colours[colour])


# Run the application
keybow2040 = Keybow2040()
pmk = PMK(keybow2040)
Hardware.set_hardware(pmk)
sequence = SequenceOfOperation()

while True:
    sequence.perform_sequence()
