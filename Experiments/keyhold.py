from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)

counter = 0

pmk.keys[0].hold_time = 0.5


@pmk.on_press(pmk.keys[0])
def press_handler(key):
    print("Keypress")


while True:
    pmk.update()
