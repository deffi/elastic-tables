from typing import Iterable


# TODO test
def grouper(n: int, iterable: Iterable, fill_value=None) -> Iterable:
    """From https://docs.python.org/3/library/itertools.html#itertools-recipes"""
    from itertools import zip_longest
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fill_value, *args)
