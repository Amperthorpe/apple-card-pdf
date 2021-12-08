
from typing import Collection
import readline


class Transaction:
    """Simple transaction class."""
    def __init__(self, date: str, desc: str, cb_percent: str, cb_amount: str, money: str) -> None:
        self.date = date
        self.desc = desc.upper()
        self.cb_percent = cb_percent.replace(' ', '')
        self.cb_amount = money_str_to_int(cb_amount)
        self.money = money_str_to_int(money)

    def __repr__(self) -> str:
        return f"Transaction({self.date}, {self.desc}, {self.cb_percent}, {self.cb_amount}, {self.money_str})"

    def _get_money_str(self) -> str:
        return money_int_to_str(self.money)
    
    def _set_money_str(self):
        self.money = money_str_to_int(self.money)

    money_str = property(_get_money_str, _set_money_str)

def remove_strs(in_str: str, remove_list: Collection[str]) -> str:
    """Remove every occurance of all strings in a collection from the input string."""
    for s in remove_list:
        out_str = in_str.replace(s, '')
    return out_str

def money_int_to_str(num_int: int) -> str:
    """Convert integer in cents into dollars string."""
    base_string = str(num_int)
    return f"${base_string[:-2]}.{base_string[-2:]}" # Not robust, should be improved.

def money_str_to_int(num_str: str) -> int:
    """Convert string in dollars into cents integer."""
    return int(remove_strs(num_str, ('.', ',', '$', ' ') )) # Not robust, should be improved.


def interactive(func):
    """Decorate a main function with command line arguments to prompt for them on run.

    Made for use with VSCode to easily add 
    """
    def inner(args):
        if "--interactive" in args:
            try: readline.read_history_file()
            except: pass
            args += input("Arguments: ").split()  # Get input args
            try: readline.write_history_file()
            except: pass
        func(args)
    return inner
