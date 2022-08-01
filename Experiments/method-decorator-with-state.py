from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

# Initialise the device
hardware = Hardware()
pmk = PMK(hardware)


class DecoratorOne:
    def __init__(self, key):
        self.member_key = key
        self.red = 0
        self.green = 255
        self.blue = 0
        self.state = "STATE"

        @pmk.on_press(self.member_key)
        def handler(a_key):
            a_key.set_led(self.red, self.green, self.blue)
            print(f"State: {self.state}")


dec = DecoratorOne(pmk.keys[0])

while True:
    pmk.update()