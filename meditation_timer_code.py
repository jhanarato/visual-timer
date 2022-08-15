from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

import meditation_timer

print("In Code.py")

hardware = Hardware()
pmk = PMK(hardware)
meditation_timer.Hardware.set_hardware(pmk)
sequence = meditation_timer.SequenceOfOperation()

while True:
    sequence.perform_sequence()