from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)

keys = pmk.keys

pattern = (0, 2, 5, 7, 8, 10, 13, 15)

while True:
    for key_index in range(0, 16):
        if key_index in pattern:
            pmk.keys[key_index].set_led(0, 255, 0)
        else:
            pmk.keys[key_index].set_led(255, 0, 0)
    pmk.update()