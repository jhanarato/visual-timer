from vtimer.actions import NextViewAction, CancelAction, OptionSelectAction
from vtimer.common import keypad, set_all_keys_colour

from vtimer.menus import Menu, MenuOption
from vtimer.timer import Timer

from vtimer.views import MinutesSelectedView, MultiplierSelectedView, AvailableOptionsView, TimerViewCycle
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
