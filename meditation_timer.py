import time
import math

key_colours = {"red": (255, 0, 0),
               "green": (0, 255, 0),
               "blue": (0, 0, 255),
               "cyan": (0, 255, 255),
               "orange": (255, 165, 0),
               "none": (0, 0, 0)}


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


class RotatedKeys:
    _pmk_to_rotated_map = {
        0: 0, 1: 4, 2: 8, 3: 12,
        4: 1, 5: 5, 6: 9, 7: 13,
        8: 2, 9: 6, 10: 10, 11: 14,
        12: 3, 13: 7, 14: 11, 15: 15
    }

    @staticmethod
    def keypad_index_to_rotated(actual):
        return RotatedKeys._pmk_to_rotated_map[actual]

    @staticmethod
    def rotated_to_keypad_index(rotated):
        actual_list = list(RotatedKeys._pmk_to_rotated_map.keys())
        rotated_list = list(RotatedKeys._pmk_to_rotated_map.values())
        index = rotated_list.index(rotated)
        return actual_list[index]


class MenuSequence:
    def __init__(self):
        self._maker = MenuMaker()
        self._minutes = 0
        self._multiplier = 0

    def do(self):
        print("Reset")
        self.reset()
        self.select_minutes()
        self.pause()
        self.select_multiplier()
        self.pause()
        self.set_timer()
        self.wait_for_keypress()

    def wait_for_keypress(self):
        wait = KeypressWait()
        wait.wait()

    def reset(self):
        hardware = Hardware.get_hardware()
        for key in hardware.keys:
            key.set_led(*key_colours["none"])

            @hardware.on_press(key)
            def handler(key):
                pass

    def select_minutes(self):
        minute_menu = self._maker.make_minutes_menu()
        minute_menu.wait_for_selection()
        minute_menu.light_selected_value()
        self._minutes = minute_menu.get_selected_value()

    def select_multiplier(self):
        multiplier_menu = self._maker.make_multiplier_menu()
        multiplier_menu.wait_for_selection()
        multiplier_menu.light_keys_up_to_selected_value()
        self._multiplier = multiplier_menu.get_selected_value()

    def pause(self):
        pause = Pause(seconds=3)
        pause.wait_until_complete()

    def set_timer(self):
        timer = Timer(self._minutes,
                      self._multiplier)

        print(f"Starting timer: {timer._minutes} x {timer._multiplier}")
        timer.start()
        monitor = TimerMonitor(timer)
        while not timer.is_complete():
            monitor.show_waiting_view()
            Hardware.get_hardware().update()

        monitor.show_complete_view()
        Hardware.get_hardware().update()


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

        menu.light_all_selectors()

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

    def light_selected_value(self):
        selected_key = self.get_selected_key()
        for selector in self._selectors:
            if selector.integer_value == selected_key.integer_value:
                selector.led_on()
            else:
                selector.led_off()

    def light_all_selectors(self):
        for selector in self._selectors:
            selector.led_on()

    def wait_for_selection(self):
        while self.get_selected_value() is None:
            Hardware.get_hardware().update()


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
            Hardware.get_hardware().update()


class Timer:
    def __init__(self, minutes, multiplier):
        self.started = False
        self._minutes = minutes
        self._multiplier = multiplier
        self._start_time_seconds = 0

    def start(self):
        self.started = True
        self._start_time_seconds = time.monotonic()

    def is_complete(self):
        return self.duration_seconds() <= self.seconds_passed()

    def duration_minutes(self):
        return self._multiplier * self._minutes

    def duration_seconds(self):
        return self.duration_minutes() * 60

    def seconds_passed(self):
        return time.monotonic() - self._start_time_seconds

    def minutes_passed(self):
        return math.floor(self.seconds_passed() / 60)

    def seconds_remaining(self):
        return self.duration_seconds() - self.seconds_passed()

    def minutes_remaining(self):
        return self.duration_minutes() - self.minutes_passed()

    def fraction_remaining(self):
        return self.seconds_remaining() / self.duration_seconds()


class TimerMonitor:
    def __init__(self, timer):
        self._timer = timer
        self._hardware = Hardware.get_hardware()
        self._mode_selector = ModeSelector()

    def show_waiting_view(self):
        mode_name = self._mode_selector.current_mode()
        if mode_name == ModeSelector.ON_INDICATOR:
            self.on_indicator_view()
        if mode_name == ModeSelector.MINUTES:
            self.minutes_view()
        if mode_name == ModeSelector.MULTIPLIER:
            self.multiplier_view()
        if mode_name == ModeSelector.COUNTDOWN:
            self.countdown_view()

    def on_indicator_view(self):
        indicator_key = 0
        for key_num in range(0, 16):
            if key_num == indicator_key:
                self._hardware.keys[key_num].set_led(*key_colours["orange"])
            else:
                self._hardware.keys[key_num].set_led(*key_colours["none"])

    def minutes_view(self):
        rotated_key = None
        colour = None

        if self._timer._minutes == 5:
            colour = "red"
            rotated_key = 0
        if self._timer._minutes == 10:
            colour = "green"
            rotated_key = 1
        if self._timer._minutes == 15:
            colour = "blue"
            rotated_key = 2

        for key_num in range(0, 16):
            if key_num == RotatedKeys.rotated_to_keypad_index(rotated_key):
                self._hardware.keys[key_num].set_led(*key_colours[colour])
            else:
                self._hardware.keys[key_num].set_led(*key_colours["none"])

    def multiplier_view(self):
        for key_num in range(0, 16):
            rotated_num = RotatedKeys.keypad_index_to_rotated(key_num)
            if rotated_num < self._timer._multiplier:
                self._hardware.keys[key_num].set_led(*key_colours["cyan"])
            else:
                self._hardware.keys[key_num].set_led(*key_colours["none"])

    def countdown_view(self):
        fraction = self._timer.fraction_remaining()
        keys_to_be_lit = 16 * fraction

        for key_num in range(0, 16):
            rotated_num = RotatedKeys.keypad_index_to_rotated(key_num)
            if key_num < keys_to_be_lit:
                self._hardware.keys[rotated_num].set_led(*key_colours["green"])
            else:
                self._hardware.keys[rotated_num].set_led(*key_colours["blue"])

    def show_complete_view(self):
        self._hardware.set_all(*key_colours["orange"])


class ModeSelector:
    ON_INDICATOR = "on_indicator"
    MINUTES = "minutes"
    MULTIPLIER = "multiplier"
    COUNTDOWN = "countdown"

    def __init__(self):
        self.modes = [ModeSelector.ON_INDICATOR,
                      ModeSelector.MINUTES,
                      ModeSelector.MULTIPLIER,
                      ModeSelector.COUNTDOWN]

        self.mode_index = 0
        hardware = Hardware.get_hardware()

        for key in hardware.keys:
            @hardware.on_press(key)
            def handler(key):
                self.next_mode()

    def next_mode(self):
        mode_name = self.modes[self.mode_index]
        self.mode_index = (self.mode_index + 1) % len(self.modes)
        return mode_name

    def current_mode(self):
        return self.modes[self.mode_index]


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
            Hardware.get_hardware().update()

        print("KeypressWait Finished")