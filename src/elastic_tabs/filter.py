from elastic_tabs import ChunkSplitter, Parser, Renderer


class Filter:
    def __init__(self):
        self.chunk_splitter = ChunkSplitter()
        self.parser = Parser()
        self.renderer = Renderer()

    def _filter(self):
        for chunk in self.chunk_splitter:
            table = self.parser.table_from_chunk(chunk)
            yield from self.renderer.render(table)

    def add_line(self, line: str):
        self.chunk_splitter.add_line(line)
        yield from self._filter()

    def flush(self):
        self.chunk_splitter.flush()
        yield from self._filter()
