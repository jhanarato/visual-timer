""" This file can be copied to code.py to demonstrate the workings of our pmk wrapper """
import time
from pmk.platform.keybow2040 import Keybow2040
from pmk import PMK
from vtimer.pmk_impl import Keypad

# Set up the PMK library
keybow2040 = Keybow2040()
pmk = PMK(keybow2040)

# Inject into the Keypad instance
keypad = Keypad(pmk)

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)


def keypress_callback(key):
    print(f"Key {key.number} pressed")


def keyhold_callback(key):
    print(f"Key {key.number} held")


keypad.set_all_keys_colour(red)
time.sleep(2)

keypad.set_keypress_function(0, keypress_callback)
keypad.set_keyhold_function(1, keyhold_callback)


keypad.set_led_colour(0, blue)
keypad.set_led_colour(1, green)

while True:
    keypad.update()
