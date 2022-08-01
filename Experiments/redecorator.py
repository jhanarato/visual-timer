from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)

the_key = pmk.keys[0]


@pmk.on_press(the_key)
def red_handler(key):
    key.set_led(255, 0, 0)

    @pmk.on_press(the_key)
    def green_handler(key):
        key.set_led(0, 255, 0)


while True:
    pmk.update()
