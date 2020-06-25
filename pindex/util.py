from time import time
from typing import List
from math import log


class Printer:
    def __init__(self, secs: int):
        self.secs = secs
        self.last_print = time() - secs
        self.last = ([], {})

    def print(self, *args, **kwargs):
        self.last = (args, kwargs)
        now = time()
        if now - self.last_print >= self.secs:
            print(*args, **kwargs)
            self.last_print = now

    def print_last(self):
        (args, kwargs) = self.last
        print(*args, **kwargs)


def human_readable(size: int) -> str:
    factor = 1000.0
    letters = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

    if size > 0:
        power = max(min(int(log(size) / log(factor)), len(letters) - 1), 0)
    else:
        power = 0

    return f"{int(size / factor**power)}{letters[power]}"


def concat(items: List[list]) -> list:
    new_list = []
    for entry in items:
        for e in entry:
            new_list.append(e)
    return new_list
