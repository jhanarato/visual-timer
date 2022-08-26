import time

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)


class PropertyKey:
    def __init__(self):
        self._key = pmk.keys[0]

    @property
    def key(self):
        self._key.set_led(255, 0, 0)
        return self._key.number

    @key.setter
    def key(self, value):
        self._key.set_led(0, 255, 0)


property_key = PropertyKey()

while True:
    pmk.update()
    _ = property_key.key
    time.sleep(1)
    pmk.update()
    property_key.key = 100
    time.sleep(1)
