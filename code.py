from vtimer.common import keypad, rotated_key_num, cycle, set_key_colour, set_all_keys_colour

from vtimer.menus import Menu, MenuOption, NOT_A_KEY_NUMBER
from vtimer.timer import Timer

from vtimer.views import MinutesSelectedView, MultiplierSelectedView, AvailableOptionsView
from vtimer.views import SimpleIndicatorView, ProgressView, TestPatternView


import time


class PrimaryInteraction:
    def __init__(self):
        self.minutes_menu = Menu()
        self.multiplier_menu = Menu()
        self.timer = Timer()

        self.cancel = CancelAction(self.timer)
        self.timer_view_cycle = TimerViewCycle(self.timer, self.create_timer_views())
        self.next_view = NextViewAction(self.timer_view_cycle)

        self.set_minutes_menu_options()
        self.set_multiplier_menu_options()

    def set_minutes_menu_options(self):
        self.minutes_menu.options = [MenuOption(0, "red", 5),
                                     MenuOption(1, "green", 10),
                                     MenuOption(2, "blue", 15)]

    def set_multiplier_menu_options(self):
        self.multiplier_menu.options = [MenuOption(key_num, "cyan", key_num + 1)
                                        for key_num in range(0, 16)]

    def create_timer_views(self):
        timer_views = [
            SimpleIndicatorView(key_num=0, colour="orange"),
            MinutesSelectedView(self.minutes_menu),
            MultiplierSelectedView(self.multiplier_menu),
            ProgressView(self.timer)
        ]

        return timer_views

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

        self.cancel.enable()
        self.next_view.enable()

        self.timer_view_cycle.cycle_while_timer_running()

        if self.timer.complete:
            set_all_keys_colour("orange")
            wait = KeypressWait()
            wait.wait()

        self.clear()

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

    def enable(self):
        for key in keypad.keys:
            @keypad.on_press(key)
            def handler(key):
                self.view_cycle.advance()


class CancelAction:
    def __init__(self, timer):
        self._timer = timer

    def enable(self):
        for key in keypad.keys:
            @keypad.on_hold(key)
            def handler(key):
                self._timer.cancelled = True


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
        while not self._menu.selection_made:
            if self._menu.option_valid_at_key(self.selected_key_num):
                self._menu.select(self.selected_key_num)
            keypad.update()


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


interaction = PrimaryInteraction()

while True:
    interaction.run()
