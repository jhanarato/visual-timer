from vtimer import set_keypad_implementation
from vtimer.interactions import PrimaryInteraction
from pmk_implementation import pmk_impl

set_keypad_implementation(pmk_impl)

interaction = PrimaryInteraction()

while True:
    interaction.run()
