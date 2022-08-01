from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK


# Exploring object-oriented programming with the Keybow2040
class Blinker(PMK):
    def __init__(self, *args, **kwargs):
        super(Blinker, self).__init__(*args, **kwargs)
        self.is_on = True

        @self.on_press(self.keys[0])
        def press_handler(key):
            if self.is_on:
                key.set_led(255, 0, 0)
            else:
                key.set_led(0, 0, 0)
            self.is_on = not self.is_on


blinker = Blinker(Hardware())

while True:
    blinker.update()
