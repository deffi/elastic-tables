from typing import List, Sequence

_unspecified = object()


def replace_value(s: Sequence, /, key, *, default=_unspecified, remove: Sequence = None) -> List:
    # Make a copy
    s = list(s)

    if key in s:
        if s.count(key) > 1:
            raise ValueError(f"Key appears multiple times: {key}")

        index = s.index(key)

        if index >= len(s) - 1:
            raise ValueError(f"No value for key: {key}")

        if remove is not None and s[index+1] in remove:
            s[index:index+2] = []
    else:
        if default is not _unspecified:
            s.extend([key, default])

    return s
