import vtimer
from vtimer.interactions import PrimaryInteraction
from pmk_implementation.pmk_impl import get_keypad

vtimer.keypad = get_keypad()

interaction = PrimaryInteraction()

while True:
    interaction.run()
