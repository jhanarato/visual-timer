from pmk.platform.keybow2040 import Keybow2040 as Hardware
from pmk import PMK

hardware = Hardware()
pmk = PMK(hardware)


class ModeSelector:
    def __init__(self):
        self.modes = ["on_indicator", "minutes", "multiplier", "countdown"]
        self.mode_index = 0

        pmk.keys[0].set_led(0, 255, 0)

        for key in pmk.keys:
            @pmk.on_press(key)
            def handler(key):
                self.next_mode()

    def next_mode(self):
        mode_name = self.modes[self.mode_index]
        print(f"Mode: {mode_name}")
        self.mode_index = (self.mode_index + 1) % len(self.modes)


selector = ModeSelector()

while True:
    pmk.update()