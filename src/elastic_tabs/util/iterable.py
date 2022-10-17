from itertools import zip_longest
from typing import Iterable


def grouper(group_size: int, iterable: Iterable, fill_value=None) -> Iterable:
    """Adapted from https://docs.python.org/3/library/itertools.html#itertools-recipes"""

    if group_size <= 0:
        raise ValueError(f"group_size must be postive, is {group_size}")

    args = [iter(iterable)] * group_size
    return zip_longest(*args, fillvalue=fill_value)
