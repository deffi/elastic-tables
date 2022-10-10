from typing import Callable, Iterable, Sequence, List

from elastic_tabs import Line
from elastic_tabs.text import split_lines


class LineSplitter:
    def __init__(self, callback: Callable[[Iterable[Line]], None] = None):
        self.callback = callback or self.enqueue

        self._buffer = ""
        self._lines: List[Line] = []

    def add(self, string: str):
        lines, remainder = split_lines(self._buffer + string)
        self._buffer = remainder
        self.callback(lines)

    def flush(self):
        self.callback([Line(self._buffer, "")])
        self._buffer = ""

    def enqueue(self, lines: Iterable[Line]):
        self._lines.extend(lines)

    def lines(self, clear: bool = True) -> Sequence[Line]:
        lines = self._lines
        if clear:
            self._lines = []
        return lines
