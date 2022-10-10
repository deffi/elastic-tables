from dataclasses import replace
from typing import Callable, Iterable, Sequence, List

from elastic_tabs import Line, Block


class BlockSplitter:
    split_on_blank_line = True
    split_on_vertical_tab = True

    def __init__(self, callback: Callable[[Block], None] = None):
        self.callback = callback or self.enqueue

        self._buffer: List[Line] = []
        self._blocks: List[Block] = []

    def add_line(self, line: Line):
        split_before = False
        split_after = False

        if self.split_on_blank_line:
            if len(line.content.strip()) == 0:
                split_after = True

        if self.split_on_vertical_tab:
            if line.content.startswith("\v"):
                replace(line, content=line.content[1:])
                split_before = True

            if line.content.endswith("\v"):
                replace(line, content=line.content[:-1])
                split_after = True

        if split_before:
            self.flush()

        self._buffer.append(line)

        if split_after:
            self.flush()

    def add_lines(self, lines: Iterable[Line]):
        for line in lines:
            self.add_line(line)

    def flush(self):
        self.callback(Block(self._buffer))
        self._buffer = []

    def enqueue(self, block: Block):
        self._blocks.append(block)

    def blocks(self, clear: bool = True) -> Sequence[Block]:
        blocks = self._blocks
        if clear:
            self._blocks = []
        return blocks
