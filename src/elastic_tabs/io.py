import sys

from elastic_tabs.filter import StreamFilter

stdout = None


def install() -> None:
    global stdout
    stdout = StreamFilter(sys.stdout)
    sys.stdout = stdout
