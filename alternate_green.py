# Make every second key green.

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)

keys = pmk.keys

while True:
    for key_indexes in range(0, 15, 2):
        pmk.keys[key_indexes].set_led(0, 255, 0)
        pmk.update()
