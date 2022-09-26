import math

from vtimer.common import all_keys, set_key_colour, cycle, keypad


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
