import re
from typing import Tuple, Sequence, Iterator

from elastic_tabs import Line
from elastic_tabs.iterable import grouper


# TODO remove
def splitlines(string: str, keep_ends: bool = False) -> Tuple[Sequence[str], str]:
    """Returns lines, remainder"""

    # str.splitlines will include unterminated lines, unless they are empty:
    #     ""           -> []
    #     "\n"         -> [""]
    #     "foo\nbar"   -> ["foo", "bar"]
    #     "foo\nbar\n" -> ["foo", "bar"]
    #
    # We want to return the unterminated part as remainder, regardless of
    # whether it is empty. So we terminate it by appending an newline and use
    # the last line as remainder. This also ensures that there will always be at
    # least one line in the result from splitlines, even if string is empty.

    # Append a newline and split
    lines = (string + "\n").splitlines(keepends=keep_ends)

    # The last line is the remainder, the others are the result
    lines, remainder = lines[:-1], lines[-1]

    # If keep_ends is true, then the remainder will include the newline we
    # appended
    if keep_ends:
        remainder = remainder[:-1]

    return lines, remainder


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
