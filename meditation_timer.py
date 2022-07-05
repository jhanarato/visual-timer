from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)

class Timer:
    def __init__(self, time_units, number_of_units):
        self.time_units = time_units
        self.number_of_units = number_of_units

    def start(self):
        minutes = self.time_units * self.number_of_units
        print(f"Timer set: {minutes} minutes")

    def is_complete(self):
        return True

timer = Timer(5, 3)
timer.start()