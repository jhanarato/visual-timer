from vtimer.keypad import AbstractKeypad

keypad = AbstractKeypad()


def set_keypad_implementation(impl):
    global keypad
    keypad = impl
