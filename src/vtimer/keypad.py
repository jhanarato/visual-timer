not_implemented_message = "Implementation must be provided before calling "


class KeypadInterface:
    def __init__(self):
        pass

    def set_keypress_function(self, key_num, fn):
        raise NotImplementedError(not_implemented_message + "set_keypress_function")

    def set_keyhold_function(self, key_num, fn):
        raise NotImplementedError(not_implemented_message + "set_keyhold_function")

    def set_led_colour(self, key_num, colour):
        raise NotImplementedError(not_implemented_message + "set_led_colour")

    def set_all_keys_colour(self, colour):
        raise NotImplementedError(not_implemented_message + "set_all_keys_colour")

    def update(self):
        raise NotImplementedError(not_implemented_message + "update")


class KeypadImplementationOwner:
    def __init__(self):
        self._keypad = KeypadInterface()

    @property
    def implementation(self):
        return self._keypad

    @implementation.setter
    def implementation(self, impl):
        self._keypad = impl


keypad_implementation = KeypadImplementationOwner()