from typing import Callable

from elastic_tabs.parsing import BlockSplitter, LineSplitter, TableGenerator
from elastic_tabs.model import Block
from elastic_tabs.rendering import Renderer


class Filter:
    def __init__(self, callback: Callable[[str], None] = None):  # TODO annotation
        self._block_splitter = BlockSplitter(self._block)
        self._line_splitter = LineSplitter(self._block_splitter.add_lines)
        self._table_generator = TableGenerator()
        self._renderer = Renderer()

        self._callback = callback or self.accumulate
        self._buffer = ""

    def accumulate(self, text: str):
        self._buffer = self._buffer + text

    def _block(self, block: Block):
        table = self._table_generator.table_from_block(block)
        text = self._renderer.render(table)
        self._callback("".join(text))

    def add_text(self, text: str):
        self._line_splitter.add(text)

    def flush(self):
        self._line_splitter.flush()
        self._block_splitter.flush()

    def text(self, clear: bool = True) -> str:
        text = self._buffer
        if clear:
            self._buffer = []
        return "".join(text)

    @classmethod
    def filter(cls, text: str) -> str:
        filter_ = cls()
        filter_.add_text(text)
        filter_.flush()
        return filter_.text()
