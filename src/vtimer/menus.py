import collections

from vtimer import events
from vtimer.util import all_keys

NOT_A_KEY_NUMBER = -2
NOT_AN_OPTION_VALUE = -1


MenuOption = collections.namedtuple("MenuOption", ["key_num", "colour", "value"])


class TooManyOptionsError(Exception):
    def __init__(self, number_of_options):
        self.number_of_options = number_of_options


class SelectionMadeEvent:
    def __init__(self, value_selected):
        self.value_selected = value_selected


class Menu:
    _not_an_option = MenuOption(key_num=NOT_A_KEY_NUMBER,
                                colour="none",
                                value=NOT_AN_OPTION_VALUE)

    def __init__(self, number_of_keys=16):
        self.number_of_keys = number_of_keys
        self._options = list()
        self.selected_option = Menu._not_an_option

    def clear_selection(self):
        self.selected_option = Menu._not_an_option

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, option_list):
        for option in option_list:
            self._options.append(option)

        self._add_missing_options()
        self._options.sort(key=lambda opt: opt.key_num)
        self._check_options()

    def _check_options(self):
        number_of_options = len(self.options)
        if number_of_options != self.number_of_keys:
            raise TooManyOptionsError(number_of_options)

        for key_num in range(0, self.number_of_keys):
            option_key_num = self.options[key_num].key_num
            if option_key_num != key_num:
                raise Exception(f"Option at index {key_num} has key_num = {option_key_num}")

    def _used_keys(self):
        return {option.key_num for option in self.options}

    def _unused_keys(self):
        return all_keys - self._used_keys()

    def _add_missing_options(self):
        for key_num in self._unused_keys():
            self._options.append(
                MenuOption(key_num=key_num,
                           colour="none",
                           value=NOT_AN_OPTION_VALUE)
            )

    def select(self, key_num):
        if self.option_valid_at_key(key_num):
            self.selected_option = self._options[key_num]
            event = SelectionMadeEvent(self.selected_option.value)
            events.post_event("menu_selection_made", event)

    @property
    def selection_made(self):
        return self.selected_option.value != NOT_AN_OPTION_VALUE

    def option_valid_at_key(self, key_num):
        if key_num not in all_keys:
            return False

        option = self.options[key_num]

        if option.value == NOT_AN_OPTION_VALUE:
            return False

        return True
