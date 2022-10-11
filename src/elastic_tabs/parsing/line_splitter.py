from typing import Callable, Iterable, Sequence, List

from elastic_tabs.model import Line
from elastic_tabs.util.text import split_lines


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
        # TODO this condition was missing, add unit test that would have caught it
        # TODO similar thing in block splitter?
        if self._buffer != "":
            self.callback([Line(self._buffer, "")])
            self._buffer = ""

    def enqueue(self, lines: Iterable[Line]):
        self._lines.extend(lines)

    def lines(self, clear: bool = True) -> Sequence[Line]:
        lines = self._lines
        if clear:
            self._lines = []
        return lines
