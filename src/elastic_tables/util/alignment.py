def left(text: str, width: int) -> str:
    return text.ljust(width)


def right(text: str, width: int) -> str:
    return text.rjust(width)


def center(text: str, width: int) -> str:
    return text.center(width)
