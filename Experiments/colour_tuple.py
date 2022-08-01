from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)

the_key = pmk.keys[0]
colour = (0, 255, 0)

the_key.set_led(*colour)