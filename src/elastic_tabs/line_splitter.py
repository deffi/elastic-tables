from typing import Callable, Iterable, Sequence, List

from elastic_tabs import Line
from elastic_tabs.text import split_lines


# TODO test
class LineSplitter:
    def __init__(self, callback: Callable[[Iterable[Line]], None] = None):
        self.callback = callback or self.enqueue

        self._buffer = ""
        self._lines: List[Line] = []

    def add(self, string: str):
        self._buffer += string
        lines, remainder = split_lines(self._buffer)
        self.callback(List[lines])

    def enqueue(self, line: Line):
        self._lines.append(line)

    def lines(self) -> Sequence[Line]:
        lines = self._lines
        self._lines = None
        return lines
