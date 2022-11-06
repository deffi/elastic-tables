import sys

from tab_les.filter import StreamFilter

stdout = None


def install() -> None:
    global stdout
    stdout = StreamFilter(sys.stdout)
    sys.stdout = stdout
