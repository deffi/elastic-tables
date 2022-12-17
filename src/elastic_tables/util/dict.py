from typing import Sequence

_unspecified = object()


# TODO unit test
def replace_value(d: dict, /, key, *, default=_unspecified, remove: Sequence = None) -> dict:
    # Make a copy
    d = dict(d)

    if key in d:
        if remove is not None and d[key] in remove:
            del d[key]
    else:
        if default is not _unspecified:
            d[key] = default

    return d
