from typing import Callable, Iterable, Sequence, List

from elastic_tabs.model import Line
from elastic_tabs.util.text import split_lines


Callback = Callable[[Iterable[Line]], None]


class LineSplitter:
    def __init__(self, callback: Callback = None):
        self._input_buffer = ""
        self._result_buffer: List[Line] = []

        self.callback: Callback = callback or self._buffer_lines

    ##################
    # Public interface
    ##################

    def input(self, string: str) -> None:
        lines, remainder = split_lines(self._input_buffer + string)
        self._input_buffer = remainder
        self.callback(lines)

    def flush(self) -> None:
        # TODO this condition was missing, add unit test that would have caught it
        # TODO similar thing in block splitter and line splitter?
        if self._input_buffer != "":
            self.callback([Line(self._input_buffer, "")])
            self._input_buffer = ""

    ###################
    # Internal buffer #
    ###################

    def _buffer_lines(self, lines: Sequence[Line]):
        self._result_buffer.extend(lines)

    def lines(self, clear: bool = True) -> Sequence[Line]:
        lines = self._result_buffer
        if clear:
            self._result_buffer = []
        return lines
