from typing import Iterable, Sequence

from elastic_tabs.parsing import BlockSplitter, LineSplitter, TableGenerator
from elastic_tabs.model import Table, Block
from elastic_tabs.rendering import Renderer

class Filter:
    def __init__(self, callback = None):  # TODO annotation
        self._block_splitter = BlockSplitter(self._block)
        self._line_splitter = LineSplitter(self._block_splitter.add_lines)
        self._table_generator = TableGenerator()
        self._renderer = Renderer()

        self._callback = callback or self.accumulate
        self._buffer = []

    def accumulate(self, text_lines: Iterable[str]):
        self._buffer.extend(text_lines)

    def _block(self, block: Block):
        table = self._table_generator.table_from_block(block)
        text = self._renderer.render(table)
        self._callback(text)

    def add_text(self, text: str):
        self._line_splitter.add(text)

    def flush(self):
        self._line_splitter.flush()
        self._block_splitter.flush()

    def text(self, clear: bool = True) -> Sequence[str]:
        text = self._buffer
        if clear:
            self._buffer = []
        return text

    @classmethod
    def filter(cls, text: str) -> Sequence[str]:
        filter_ = cls()
        filter_.add_text(text)
        filter_.flush()
        return filter_.text()
