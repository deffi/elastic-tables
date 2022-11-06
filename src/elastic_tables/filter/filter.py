from typing import Callable

from elastic_tables.parsing import BlockSplitter, LineSplitter, TableGenerator
from elastic_tables.model import Block
from elastic_tables.rendering import Renderer


Callback = Callable[[str], None]


class Filter:
    def __init__(self, callback: Callback = None):
        self._block_splitter = BlockSplitter(self._input_block)
        self._line_splitter = LineSplitter(self._block_splitter.input)
        self._table_generator = TableGenerator()
        self._renderer = Renderer()

        self._callback = callback or self._buffer_result
        self._result_buffer = ""

    @classmethod
    def filter(cls, text: str) -> str:
        filter_ = cls()
        filter_.input(text)
        filter_.flush()
        return filter_.text()

    ##############
    # Processing #
    ##############

    def _input_block(self, block: Block) -> None:
        table = self._table_generator.table_from_block(block)
        text = self._renderer.render(table)
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
