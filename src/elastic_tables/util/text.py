import re
from typing import Tuple, Iterator

from elastic_tables.model import Line
from elastic_tables.util.iterable import grouper


def split_lines(string: str) -> Tuple[Iterator[Line], str]:
    """Splits a string into lines and returns a tuple of:
      * An iterator that yields Line instances for terminated lines
      * An str that contains the remainder of the string (potentially empty)

    Recognizes \r and \r\n as line terminators.
    """

    # Examples:
    #     ["foo", "\n", "bar"]
    #     ["foo", "\n", "bar", "\n"]
    parts = re.split(r"(\r?\n)", string)

    # An odd number means that the last line is unterminated
    if len(parts) % 2 != 0:
        (*parts, remainder) = parts
    else:
        remainder = ""

    pairs = grouper(2, parts, None)
    lines = (Line(content, terminator) for content, terminator in pairs)

    return lines, remainder
