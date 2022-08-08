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
    def set_key_colour(key_num, colour, rotated=False):
        if rotated:
            key_num = Hardware.rotator.to_device_orientation(key_num)
        Hardware._pmk.keys[key_num].set_led(*key_colours[colour])

    @staticmethod
    def set_all_colour(colour):
        Hardware._pmk.set_all(*key_colours[colour])

    @staticmethod
    def any_key_pressed():
        Hardware.update()
        return Hardware._pmk.any_pressed()

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


class MenuSequence:
    def __init__(self):
        self._maker = MenuMaker()
        self._minutes = 0
        self._multiplier = 0

    def do(self):
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
        Hardware.reset()

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
        pause = Pause(seconds=1.5)
        pause.wait_until_complete()

    def set_timer(self):
        timer = Timer(self._minutes,
                      self._multiplier)

        print(f"Starting timer: {timer.get_minutes()} x {timer.get_multiplier()}")

        timer.start()
        monitor = TimerMonitor(timer)
        while not timer.is_complete():
            monitor.show_waiting_view()
            Hardware.update()

        monitor.show_complete_view()
        Hardware.update()


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
            Hardware.update()


class IntegerSelector:
    def __init__(self, rotated_key_index, integer_value):
        self.integer_value = integer_value
        self._rotated_key_index = rotated_key_index
        self.selected = False
        self._on_colour = "none"
        self._off_colour = "none"

    def set_colour(self, colour):
        self._on_colour = colour

    def enable_keypress(self):
        hardware = Hardware.get_hardware()
        key = Hardware.get_rotated_key(self._rotated_key_index)

        @hardware.on_press(key)
        def select(choice_key):
            self.selected = True

    def led_on(self):
        Hardware.set_key_colour(self._rotated_key_index, self._on_colour, rotated=True)

    def led_off(self):
        Hardware.set_key_colour(self._rotated_key_index, self._off_colour, rotated=True)


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


class TimerMonitor:
    def __init__(self, timer):
        self._timer = timer
        self.modes = ModeSelector()

        hardware = Hardware.get_hardware()

        for key in hardware.keys:
            @hardware.on_press(key)
            def handler(key):
                self.modes.next()

    def show_waiting_view(self):
        mode = self.modes.current()

        if mode == ModeSelector.ON_INDICATOR:
            self.on_indicator_view()
        if mode == ModeSelector.MINUTES:
            self.minutes_view()
        if mode == ModeSelector.MULTIPLIER:
            self.multiplier_view()
        if mode == ModeSelector.COUNTDOWN:
            self.countdown_view()

    def on_indicator_view(self):
        indicator_key = 0
        for key_num in range(0, 16):
            if key_num == indicator_key:
                Hardware.set_key_colour(key_num, "orange", rotated=False)
            else:
                Hardware.set_key_colour(key_num, "none", rotated=False)

    def minutes_view(self):
        minutes = self._timer.get_minutes()

        all_keys = set(range(0, 16))
        selected = set()

        if minutes == 5:
            selected.add(0)
            Hardware.set_key_colour(0, "red", rotated=True)
        if minutes == 10:
            selected.add(1)
            Hardware.set_key_colour(1, "green", rotated=True)
        if minutes == 15:
            selected.add(2)
            Hardware.set_key_colour(2, "blue", rotated=True)

        not_selected = all_keys - selected

        for key_num in not_selected:
            Hardware.set_key_colour(key_num, "none", rotated=True)

    def multiplier_view(self):
        multiplier = self._timer.get_multiplier()

        all_keys = set(range(0, 16))
        selected = set(range(0, multiplier))
        not_selected = all_keys - selected

        for key_num in selected:
            Hardware.set_key_colour(key_num, "cyan", rotated=True)

        for key_num in not_selected:
            Hardware.set_key_colour(key_num, "none", rotated=True)

    def countdown_view(self):
        fraction = self._timer.fraction_remaining()
        keys_to_be_lit = math.ceil(16 * fraction)

        all_keys = set(range(0, 16))
        green_keys = set(range(0, keys_to_be_lit))
        blue_keys = all_keys - green_keys

        for key_num in green_keys:
            Hardware.set_key_colour(key_num, "green", rotated=True)

        for key_num in blue_keys:
            Hardware.set_key_colour(key_num, "blue", rotated=True)

    def show_complete_view(self):
        Hardware.set_all_colour("orange")


class ModeSelector:
    ON_INDICATOR = 0
    MINUTES = 1
    MULTIPLIER = 2
    COUNTDOWN = 3

    def __init__(self):
        self.modes = [ModeSelector.ON_INDICATOR,
                      ModeSelector.MINUTES,
                      ModeSelector.MULTIPLIER,
                      ModeSelector.COUNTDOWN]

        self.mode_index = 0

    def next(self):
        self.mode_index = (self.mode_index + 1) % len(self.modes)

    def current(self):
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


class Timer:
    def __init__(self, minutes, multiplier):
        self.started = False
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