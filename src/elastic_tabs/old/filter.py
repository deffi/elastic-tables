from typing import Iterable, Iterator

from elastic_tabs.old import ChunkSplitter, Parser, Renderer


class Filter:
    def __init__(self):
        self.chunk_splitter = ChunkSplitter()
        self.parser = Parser()
        self.renderer = Renderer()

    def render_tables(self) -> Iterator[str]:
        for chunk in self.chunk_splitter:
            table = self.parser.table_from_chunk(chunk)
            yield from self.renderer.render(table)

    def add_line(self, line: str):
        self.chunk_splitter.add_line(line)

    def add_lines(self, lines: Iterable[str]):
        self.chunk_splitter.add_lines(lines)

    def flush(self):
        self.chunk_splitter.flush()

    @classmethod
    def filter(cls, text: str) -> str:
        filter_ = cls()
        filter_.add_lines(text.splitlines())
        filter_.flush()
        return "\n".join(filter_.render_tables())
