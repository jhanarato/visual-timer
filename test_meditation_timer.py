import time

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

import meditation_timer

hardware = Hardware()
pmk = PMK(hardware)


class ValueChangeMonitor:
    def __init__(self):
        self._old_value = None
        self._changed = False

    def update_value(self, new_value):
        if new_value is not None:
            if self._old_value != new_value:
                self._old_value = new_value
                self._changed = True

    def value_has_changed(self):
        if self._changed:
            self._changed = False
            return True
        else:
            return False


class Pause:
    def __init__(self, seconds):
        self._seconds_to_pause_for = seconds
        self._start = time.monotonic()

    def complete(self):
        now = time.monotonic()
        paused_for = now - self._start
        return paused_for > self._seconds_to_pause_for


def test_minutes_menu():
    print("In test_minutes_menu()")
    meditation_timer.Hardware.set_hardware(pmk)
    maker = meditation_timer.MenuMaker()
    minute_menu = maker.make_minutes_menu()

    while True:
        if minute_menu.get_selected_value() is not None:
            pmk.update()
            break
        pmk.update()

    minute_menu.light_selected_value()

    pause = Pause(seconds=3)

    while not pause.complete():
        pmk.update()

    print(f"Minutes Menu Selection: {minute_menu.get_selected_value()}")


def test_multiplier_menu():
    print("In test_multiplier_menu()")
    meditation_timer.Hardware.set_hardware(pmk)
    maker = meditation_timer.MenuMaker()
    multiplier_menu = maker.make_multiplier_menu()
    multiplier_menu.light_all_selectors()

    while True:
        if multiplier_menu.get_selected_value() is not None:
            pmk.update()
            break
        pmk.update()

    multiplier_menu.light_keys_up_to_selected_value()

    pause = Pause(seconds=3)

    while not pause.complete():
        pmk.update()

    print(f"Multiplier Menu Selection: {multiplier_menu.get_selected_value()}")


def test_integer_selector():
    meditation_timer.Hardware.set_hardware(pmk)

    selector = meditation_timer.IntegerSelector(rotated_key_index=0, integer_value=1)
    selector.set_colour("orange")
    selector.enable_keypress()
    selector.led_on()

    message_printed = False
    while True:
        if selector.selected and not message_printed:
            print(f"Integer {selector.integer_value} selected")
            message_printed = True
        pmk.update()


def test_rotated_keys():
    print("Test 1")
    turn_on = True
    while True:
        for pmk_number in range(0, 16):
            rotated_number = meditation_timer.RotatedKeys.keypad_index_to_rotated(pmk_number)
            if turn_on:
                pmk.keys[rotated_number].set_led(0, 255, 0)
            else:
                pmk.keys[rotated_number].set_led(0, 0, 0)
            time.sleep(0.2)
            pmk.update()

        turn_on = not turn_on


def test_menus_in_sequence():
    # TODO: Break up steps and move to MenuSequence class
    print("In test_menus_in_sequence()")
    meditation_timer.Hardware.set_hardware(pmk)
    maker = meditation_timer.MenuMaker()

    # Step 1: Select minutes
    minute_menu = maker.make_minutes_menu()

    while minute_menu.get_selected_value() is None:
        pmk.update()

    minute_menu.light_selected_value()

    # Step 2: Wait for 3 seconds
    pause = Pause(seconds=3)
    while not pause.complete():
        pmk.update()

    # Step 3: Select multiplier
    multiplier_menu = maker.make_multiplier_menu()

    while multiplier_menu.get_selected_value() is None:
        pmk.update()

    multiplier_menu.light_keys_up_to_selected_value()

    # Step 4: Wait for 3 seconds.
    pause = Pause(seconds=3)
    while not pause.complete():
        pmk.update()

    # Step 5: Now we have our values, print them to the console.
    minutes = minute_menu.get_selected_value()
    multiplier = multiplier_menu.get_selected_value()
    total_time = minutes * multiplier

    print(f"Minutes: {minutes}, Multiplier: {multiplier}, Total Time: {total_time}")


def test_sequence():
    print("In test_sequence()")
    meditation_timer.Hardware.set_hardware(pmk)
    sequence = meditation_timer.MenuSequence()
    while True:
        sequence.do()


# test_minutes_menu()
# test_multiplier_menu()
# test_integer_selector()
# test_rotated_keys()
# test_menus_in_sequence()
test_sequence()