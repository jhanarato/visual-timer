from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)


class Timer:
    def __init__(self):
        self.is_set = False
        self.time_units = 0
        self.number_of_units = 0

    def start(self):
        minutes = self.time_units * self.number_of_units
        print(f"Timer set: {minutes} minutes")
        self.is_set = True

    def is_complete(self):
        # TODO Check if the time has elapsed.
        return self.is_set


# TODO Refactor this function.
def show_unit_options():
    five_min_key = pmk.keys[0]
    ten_min_key = pmk.keys[4]
    fifteen_min_key = pmk.keys[8]

    five_min_key.set_led(255, 0, 0)
    ten_min_key.set_led(0, 255, 0)
    fifteen_min_key.set_led(0, 0, 255)

    @pmk.on_press(five_min_key)
    def five_handler(key):
        timer.time_units = 5
        timer.start()

    @pmk.on_press(ten_min_key)
    def ten_handler(key):
        timer.time_units = 10
        timer.start()

    @pmk.on_press(fifteen_min_key)
    def fifteen_handler(key):
        timer.time_units = 15
        timer.start()


timer = Timer()

# TODO User selects the number to multiply the units.
timer.number_of_units = 3
show_unit_options()

msg_shown = False
while True:
    # We only want to print the message once
    if not msg_shown and timer.is_complete():
        print("Time's up")
        msg_shown = True

    pmk.update()
