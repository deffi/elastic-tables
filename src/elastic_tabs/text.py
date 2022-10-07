from typing import Tuple, Sequence


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
