# This is my very first script.

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)

while True:
    pmk.set_all(255, 0, 255)
    pmk.update()