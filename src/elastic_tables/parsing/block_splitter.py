from dataclasses import replace
from typing import Callable, Iterable, Sequence, List

from elastic_tables.model import Line, Block


Callback = Callable[[Block], None]


class BlockSplitter:
    split_on_blank_line = True
    split_on_vertical_tab = True

    def __init__(self, callback: Callable[[Block], None] = None):
        self._input_buffer: List[Line] = []
        self._result_buffer: List[Block] = []

        self._callback: Callback = callback or self._buffer_block

    ##############
    # Processing #
    ##############

    def _add_line(self, line: Line) -> None:
        split_before = False
        split_after = False

        if self.split_on_blank_line:
            if len(line.content.strip()) == 0:
                split_after = True

        if self.split_on_vertical_tab:
            if line.content.startswith("\v"):
                line = replace(line, content=line.content[1:])
                split_before = True

            if line.content.endswith("\v"):
                line = replace(line, content=line.content[:-1])
                split_after = True

        if split_before:
            self.flush()

        self._input_buffer.append(line)

        if split_after:
            self.flush()

    ####################
    # Public interface #
    ####################

    def input(self, lines: Iterable[Line]) -> None:
        for line in lines:
            self._add_line(line)

    def flush(self) -> None:
        if len(self._input_buffer) != 0:
            self._callback(Block(self._input_buffer))
            self._input_buffer = []

    ###################
    # Internal buffer #
    ###################

    def _buffer_block(self, block: Block):
        self._result_buffer.append(block)

    def blocks(self, clear: bool = True) -> Sequence[Block]:
        blocks = self._result_buffer
        if clear:
            self._result_buffer = []
        return blocks
