from dataclasses import replace
from typing import Callable

from elastic_tables.parsing import BlockSplitter, LineSplitter
from elastic_tables.model import Block, Table, Cell
from elastic_tables.util import alignment

Callback = Callable[[str], None]


class Filter:
    def __init__(self, callback: Callback = None):
        self.align_numeric = False
        self.align_space = False

        self._block_splitter = BlockSplitter(self._input_block)
        self._line_splitter = LineSplitter(self._block_splitter.input)

        self._callback = callback or self._buffer_result
        self._result_buffer = ""

    @classmethod
    def filter(cls, text: str, align_numeric: bool = None, align_space: bool = None) -> str:
        filter_ = cls()

        if align_numeric is not None:
            filter_.align_numeric = align_numeric
        if align_space is not None:
            filter_.align_space = align_space

        filter_.input(text)
        filter_.flush()

        return filter_.text()

    ##############
    # Processing #
    ##############

    @staticmethod
    def align_cell_space(cell: Cell) -> Cell:
        # TODO clarify blank cell
        # TODO clarify existing alignment
        if cell.text == " " * len(cell):
            return replace(cell, text=" " * max(len(cell) - 2, 0), alignment = None)
        elif cell.text.startswith(" ") and cell.text.endswith(" "):
            return replace(cell, text=cell.text[1:-1], alignment=alignment.center)
        elif cell.text.startswith(" "):
            return replace(cell, text=cell.text[1:], alignment=alignment.right)
        elif cell.text.endswith(" "):
            return replace(cell, text=cell.text[:-1], alignment=alignment.left)
        else:
            return cell

    def _input_block(self, block: Block) -> None:
        table = Table.from_block(block)
        if self.align_numeric:
            table = table.align_numeric()
        if self.align_space:
            table = table.map_cells(self.align_cell_space)
        text = table.render()
        self._callback("".join(text))

    ####################
    # Public interface #
    ####################

    def input(self, text: str) -> None:
        self._line_splitter.input(text)

    def flush(self) -> None:
        self._line_splitter.flush()
        self._block_splitter.flush()

    ###################
    # Internal buffer #
    ###################

    def _buffer_result(self, text: str) -> None:
        self._result_buffer = self._result_buffer + text

    def text(self, clear: bool = True) -> str:
        text = self._result_buffer
        if clear:
            self._result_buffer = []
        return "".join(text)
