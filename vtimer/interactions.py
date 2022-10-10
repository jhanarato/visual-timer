from vtimer.util import Pause
from vtimer.actions import enable_keypress_action, enable_hold_action
from vtimer.actions import CancelAction, NextViewAction, OptionSelectAction, KeypressWaitAction
from vtimer.menus import Menu, MenuOption
from vtimer.timer import Timer

from vtimer.views import SimpleIndicatorView, ProgressView, TestPatternView, TimerCompleteView
from vtimer.views import AvailableOptionsView, MinutesSelectedView, MultiplierSelectedView
from vtimer.views import TimerViewCycle


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

        enable_hold_action(self.cancel)
        enable_keypress_action(self.next_view)

        self.timer_view_cycle.cycle_while_timer_running()

        if self.timer.complete:
            complete_view = TimerCompleteView()
            complete_view.display()
            wait = KeypressWaitAction()
            wait.wait()

        self.clear()

    def clear(self):
        self.minutes_menu.clear_selection()
        self.multiplier_menu.clear_selection()
        self.timer.reset()
        self.timer_view_cycle.reset()


class MenuInteraction:
    def __init__(self, menu):
        self._menu = menu
        self.selected_view = TestPatternView()

    def begin(self):
        available_options_view = AvailableOptionsView(self._menu.options)
        available_options_view.display()

        select_action = OptionSelectAction(self._menu)
        enable_keypress_action(select_action)
        select_action.wait_for_selection()

        self.selected_view.display()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()
        print("Interaction ended 1010")
