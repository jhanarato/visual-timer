from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

from src import code as mt

print("Testing Hardware")

print("Initialising")
hardware = Hardware()
pmk = PMK(hardware)
mt.Hardware.set_hardware(pmk)

print("Displaying normal layout")
for key_num in range(0, 5):
    mt.Hardware.set_rotated_key_colour(key_num, "blue", rotated=True)

