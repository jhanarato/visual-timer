import time
import math

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

        minutes = self.select_minutes()
        multiplier = self.select_multiplier()

        timer = self.start_timer(minutes, multiplier)
        self.monitor_timer(timer)

        if timer.is_cancelled():
            return

        self.show_complete_view()

        wait = KeypressWait()
        wait.wait()

    def select_minutes(self):
        minute_menu = make_minutes_menu()

        minute_menu.wait_for_selection()
        minute_menu.light_selected_option_key()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()

        return minute_menu.get_selected().integer_value

    def select_multiplier(self):
        multiplier_menu = make_multiplier_menu()

        multiplier_menu.wait_for_selection()
        multiplier_menu.light_up_to_selected_option_key()

        pause = Pause(seconds=1.5)
        pause.wait_until_complete()

        return multiplier_menu.get_selected().integer_value

    def start_timer(self, minutes, multiplier):
        timer = Timer(minutes, multiplier)
        print(f"Starting timer: {minutes} x {multiplier}")
        timer.start()
        return timer

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
            Hardware.set_rotated_key_colour(key_num, "orange")
        Hardware.update()


def make_minutes_menu():
    menu = Menu()

    menu.create_option(0, "red", 5)
    menu.create_option(1, "green", 10)
    menu.create_option(2, "blue", 15)

    menu.light_all_option_keys()

    return menu


def make_multiplier_menu():
    menu = Menu()

    for index in range(0, 16):
        multiplier_value = index + 1
        menu.create_option(index, "cyan", multiplier_value)

    menu.light_all_option_keys()

    return menu


class Menu:
    def __init__(self):
        self._options = dict()

        self.enable_choice_on_keypress()
        self._selected = None

    def add_option(self, option):
        self._options[option.key_num] = option

    def create_option(self, rotated_key_index, colour, integer_value):
        option = MenuOption(rotated_key_index, colour, integer_value)
        self.add_option(option)

    def enable_choice_on_keypress(self):
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

        self._set_selected(rotated)

    def _set_selected(self, rotated_key_index):
        self._selected = self._options.get(rotated_key_index)

    def get_selected(self):
        return self._selected

    def wait_for_selection(self):
        while self.get_selected() is None:
            Hardware.update()

    def light_selected_option_key(self):
        selected = self.get_selected()
        for option in self._get_all_options():
            if option == selected:
                option.led_on()
            else:
                option.led_off()

    def _get_all_options(self):
        return self._options.values()

    def light_up_to_selected_option_key(self):
        for option in self._get_all_options():
            if option <= self.get_selected():
                option.led_on()
            else:
                option.led_off()

    def light_all_option_keys(self):
        for selector in self._get_all_options():
            selector.led_on()


class MenuOption:
    def __init__(self, key_num, colour, integer_value):
        self.key_num = key_num
        self.colour = colour
        self.integer_value = integer_value

    def led_on(self):
        Hardware.set_rotated_key_colour(self.key_num, self.colour)

    def led_off(self):
        Hardware.set_rotated_key_colour(self.key_num, "none")

    def __le__(self, other):
        return self.integer_value <= other.integer_value

    def __eq__(self, other):
        return self.integer_value == other.integer_value

    def __str__(self):
        return f"rotated key {self.key_num} colour {self.colour} value {self.integer_value}"


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
            Hardware.set_rotated_key_colour(key_num, "orange")

        for key_num in not_selected:
            Hardware.set_rotated_key_colour(key_num, "none")

    def show_minutes_view(self):
        minutes = self._timer.get_minutes()
        selected = set()

        if minutes == 5:
            selected.add(0)
            Hardware.set_rotated_key_colour(0, "red")
        if minutes == 10:
            selected.add(1)
            Hardware.set_rotated_key_colour(1, "green")
        if minutes == 15:
            selected.add(2)
            Hardware.set_rotated_key_colour(2, "blue")

        not_selected = all_keys - selected

        for key_num in not_selected:
            Hardware.set_rotated_key_colour(key_num, "none")

    def show_multiplier_view(self):
        multiplier = self._timer.get_multiplier()
        selected = set(range(0, multiplier))
        not_selected = all_keys - selected

        for key_num in selected:
            Hardware.set_rotated_key_colour(key_num, "cyan")

        for key_num in not_selected:
            Hardware.set_rotated_key_colour(key_num, "none")

    def show_progress_view(self):
        fraction = self._timer.fraction_remaining()
        keys_to_be_lit = math.ceil(16 * fraction)
        green_keys = set(range(0, keys_to_be_lit))
        blue_keys = all_keys - green_keys

        for key_num in green_keys:
            Hardware.set_rotated_key_colour(key_num, "green")

        for key_num in blue_keys:
            Hardware.set_rotated_key_colour(key_num, "blue")


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
    def set_rotated_key_colour(key_num, colour):
        key_num = Hardware.rotator.to_device_orientation(key_num)
        Hardware._pmk.keys[key_num].set_led(*key_colours[colour])

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