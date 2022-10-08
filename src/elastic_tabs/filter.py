from typing import Iterable

from elastic_tabs import ChunkSplitter, Parser, Renderer


class Filter:
    def __init__(self):
        self.chunk_splitter = ChunkSplitter()
        self.parser = Parser()
        self.renderer = Renderer()

    def render_tables(self):
        for chunk in self.chunk_splitter:
            table = self.parser.table_from_chunk(chunk)
            yield from self.renderer.render(table)

    def add_line(self, line: str):
        self.chunk_splitter.add_line(line)

    def add_lines(self, lines: Iterable[str]):
        self.chunk_splitter.add_lines(lines)

    def flush(self):
        self.chunk_splitter.flush()
