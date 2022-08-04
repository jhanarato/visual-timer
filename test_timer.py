from meditation_timer import Timer, key_colours

from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)


timer = Timer()
timer.minutes = 1
timer.multiplier = 5
timer.start()

remaining = timer.minutes_remaining()
print(f"Remaining: {remaining}")

while not timer.is_complete():
    remaining = timer.minutes_remaining()
    for key_num in range(0, 16):
        if key_num < remaining:
            pmk.keys[key_num].set_led(*key_colours["green"])
        else:
            pmk.keys[key_num].set_led(*key_colours["blue"])
    pmk.update()

pmk.set_all(*key_colours["orange"])