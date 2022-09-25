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


class PrimaryInteraction:
    def __init__(self):
        self.minutes_menu = Menu()
        self.multiplier_menu = Menu()
        self.timer = Timer()

        self.set_minutes_menu_options()
        self.set_multiplier_menu_options()

    def set_minutes_menu_options(self):
        self.minutes_menu.options = [MenuOption(0, "red", 5),
                                     MenuOption(1, "green", 10),
                                     MenuOption(2, "blue", 15)]

    def set_multiplier_menu_options(self):
        self.multiplier_menu.options = [MenuOption(key_num, "cyan", key_num + 1)
                                        for key_num in range(0, 16)]

    def run(self):
        minutes_interaction = MenuInteraction(self.minutes_menu)
        minutes_interaction.selected_view = MinutesSelectedView(self.minutes_menu)
        minutes_interaction.begin()
        self.timer.minutes = self.minutes_menu.selected_option.value

        multiplier_interaction = MenuInteraction(self.multiplier_menu)
        multiplier_interaction.selected_view = MultiplierSelectedView(self.multiplier_menu)
        multiplier_interaction.begin()
        self.timer.multiplier = self.multiplier_menu.selected_option.value

        self.timer.start()

        cancel = CancelAction(self.timer)

        timer_views = self.create_timer_views()

        timer_view_cycle = TimerViewCycle(self.timer, timer_views)

        next_view = NextViewAction(timer_view_cycle)

        timer_view_cycle.cycle_while_timer_running()

        if self.timer.complete:
            set_all_keys_colour("orange")
            wait = KeypressWait()
            wait.wait()

        self.clear()

    def create_timer_views(self):
        timer_views = [
            SimpleIndicatorView(key_num=0, colour="orange"),
            MinutesSelectedView(self.minutes_menu),
            MultiplierSelectedView(self.multiplier_menu),
            ProgressView(self.timer)
        ]

        return timer_views

    def clear(self):
        self.minutes_menu.clear_selection()
        self.multiplier_menu.clear_selection()
        self.timer.reset()


class MenuInteraction:
    def __init__(self, menu):
        self._menu = menu
        self.selected_view = TestPatternView()

    def begin(self):
        available_options_view = AvailableOptionsView(self._menu.options)
        available_options_view.display()

        select_action = OptionSelectAction(self._menu)
        select_action.wait_for_selection()

        self.selected_view.display()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()


class TimerViewCycle:
    def __init__(self, timer, views):
        self._timer = timer
        self._views_iter = cycle(views)
        self._current_view = self._next_view()

    def _next_view(self):
        return next(self._views_iter)

    def advance(self):
        self._current_view = self._next_view()

    def cycle_while_timer_running(self):
        while self._timer.running:
            self._current_view.display()
            keypad.update()


class NextViewAction:
    def __init__(self, view_cycle):
        self.view_cycle = view_cycle
        self._enable_on_press()

    def _enable_on_press(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(key):
                self.view_cycle.advance()


class CancelAction:
    def __init__(self, timer):
        self._timer = timer
        self.enable_on_hold()

    def enable_on_hold(self):
        for key in keypad.keys:
            @keypad.on_hold(key)
            def handler(key):
                self._timer.cancelled = True


class Timer:
    def __init__(self):
        self.minutes = 0
        self.multiplier = 0
        self.started = False
        self.cancelled = False
        self._start_time_seconds = 0

    def start(self):
        self.started = True
        self.cancelled = False
        self._start_time_seconds = time.monotonic()
        print(f"Timer set: {self.minutes} x {self.multiplier} = {self.total_minutes()} minutes")

    @property
    def complete(self):
        return self.total_seconds() <= self.seconds_passed()

    @property
    def running(self):
        return self.started and not self.complete and not self.cancelled

    def reset(self):
        self.minutes = 0
        self.multiplier = 0
        self.started = False
        self.cancelled = False
        self._start_time_seconds = 0

    def total_minutes(self):
        return self.multiplier * self.minutes

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


MenuOption = collections.namedtuple("MenuOption", ["key_num", "colour", "value"])


class Menu:
    _not_an_option = MenuOption(key_num=NOT_A_KEY_NUMBER,
                                colour="none",
                                value=NOT_AN_OPTION_VALUE)

    def __init__(self, number_of_keys=16):
        self.number_of_keys = number_of_keys
        self._options = list()
        self.selected_option = Menu._not_an_option

    def clear_selection(self):
        self.selected_option = Menu._not_an_option

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, option_list):
        for option in option_list:
            self._options.append(option)

        self._add_missing_options()
        self._options.sort(key=lambda opt: opt.key_num)
        self._check_options()

    def _check_options(self):
        number_of_options = len(self.options)
        if number_of_options != self.number_of_keys:
            raise Exception(f"Menu has {number_of_options} options. ")

        for key_num in range(0, self.number_of_keys):
            option_key_num = self.options[key_num].key_num
            if option_key_num != key_num:
                raise Exception(f"Option at index {key_num} has key_num = {option_key_num}")

    def _used_keys(self):
        return {option.key_num for option in self.options}

    def _unused_keys(self):
        return all_keys - self._used_keys()

    def _add_missing_options(self):
        for key_num in self._unused_keys():
            self._options.append(
                MenuOption(key_num=key_num,
                           colour="none",
                           value=NOT_AN_OPTION_VALUE)
            )


class OptionSelectAction:
    def __init__(self, menu):
        self._menu = menu
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

    def wait_for_selection(self):
        while True:
            keypad.update()
            key_num = self.selected_key_num
            if key_num in all_keys:
                option = self._menu.options[key_num]
                if option.value is not NOT_AN_OPTION_VALUE:
                    self._menu.selected_option = option
                    return


class AvailableOptionsView:
    def __init__(self, options):
        self._options = options

    def display(self):
        for option in self._options:
            set_key_colour(option.key_num, option.colour)


class MinutesSelectedView:
    def __init__(self, menu):
        self._menu = menu

    def display(self):
        selected_key = self._menu.selected_option.key_num
        colour = self._menu.selected_option.colour
        other_keys = all_keys - {self._menu.selected_option.key_num}

        set_key_colour(selected_key, colour)

        for key_num in other_keys:
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


class SimpleIndicatorView:
    def __init__(self, key_num, colour):
        self._indicator_key_num = key_num
        self._colour = colour

    def _unused_keys(self):
        return all_keys - {self._indicator_key_num}

    def display(self):
        set_key_colour(self._indicator_key_num, self._colour)

        for key_num in self._unused_keys():
            set_key_colour(key_num, "none")


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


class TestPatternView:
    def __init__(self):
        self._pattern = [
            0, 1, 0, 1,
            1, 0, 1, 0,
            0, 1, 0, 1,
            1, 0, 1, 0
        ]

    def display(self):
        for key_num in range(0, 16):
            if self._pattern[key_num] == 0:
                colour = "green"
            else:
                colour = "red"

            set_key_colour(key_num, colour)


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


def cycle(iterable):
    """ A simple implementation of itertools.cycle() """
    while True:
        for element in iterable:
            yield element


interaction = PrimaryInteraction()
while True:
    interaction.run()
