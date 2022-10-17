import sys

from elastic_tabs.filter import StreamFilter

stdout = None


def install():
    global stdout
    stdout = StreamFilter(sys.stdout)
    sys.stdout = stdout
