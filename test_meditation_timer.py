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


def test_minutes_menu():
    meditation_timer.Hardware.set_hardware(pmk)

    maker = meditation_timer.MenuMaker()
    menu = maker.make_minutes_menu()

    monitor = ValueChangeMonitor()
    while True:
        minutes = menu.get_selected_value()
        monitor.update_value(minutes)
        if monitor.value_has_changed():
            print(f"Minutes set to: {minutes}")
            menu.reset_menu()
        pmk.update()


def test_multiplier_menu():
    meditation_timer.Hardware.set_hardware(pmk)

    maker = meditation_timer.MenuMaker()
    menu = maker.make_multiplier_menu()

    monitor = ValueChangeMonitor()

    while True:
        multiplier = menu.get_selected_value()
        monitor.update_value(multiplier)
        if monitor.value_has_changed():
            menu.light_keys_up_to_selected_value()
            print(f"Multiplier set to: {multiplier}")
            menu.reset_menu()
        pmk.update()


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


# test_minutes_menu()
# test_multiplier_menu()
# test_integer_selector()
test_rotated_keys()
