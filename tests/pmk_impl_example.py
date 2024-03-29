""" This file can be copied to code.py to demonstrate the workings of our pmk wrapper """
import time
from pmk_implementation.pmk_impl import get_keypad

keypad_impl = get_keypad()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


def keypress_callback(key):
    print(f"Key {key.number} pressed")


def keyhold_callback(key):
    print(f"Key {key.number} held")


keypad_impl.set_all_keys_colour(red)
time.sleep(2)

keypad_impl.set_keypress_function(0, keypress_callback)
keypad_impl.set_keyhold_function(1, keyhold_callback)


keypad_impl.set_led_colour(0, blue)
keypad_impl.set_led_colour(1, green)

while True:
    keypad_impl.update()
