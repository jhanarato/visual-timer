from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK


class XCallback:
    def __init__(self, x):
        self._x = x

    def __call__(self, a_key):
        a_key.led_on()
        print(self._x)


hardware = Hardware()
pmk = PMK(hardware)

keys = pmk.keys

key = keys[0]
rgb = (255, 255, 0)
key.rgb = rgb

callback = XCallback("Called!")
key.press_function = callback

while True:
    pmk.update()