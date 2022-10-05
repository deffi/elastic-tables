from typing import Iterator, Iterable, List

# TODO multiple consecutive blank lines should be a single chunk

class ChunkSplitter:
    split_on_blank_line = True
    split_on_vertical_tab = True

    def __init__(self):
        self._chunks: List[List[str]] = []
        self._current_chunk: List[str] = []

    def add_line(self, line: str):
        split_before = False
        split_after = False

        if self.split_on_blank_line:
            if len(line.strip()) == 0:
                split_after = True

        if self.split_on_vertical_tab:
            if line.startswith("\v"):
                line = line[1:]
                split_before = True

            if line.endswith("\v"):
                line = line[:-1]
                split_after = True

        if split_before:
            self.flush()

        self._current_chunk.append(line)

        if split_after:
            self.flush()

    def add_lines(self, lines: Iterable[str]):
        for line in lines:
            self.add_line(line)

    def flush(self):
        self._chunks.append(self._current_chunk)
        self._current_chunk = []

    def __iter__(self) -> Iterator[List[str]]:
        chunks = self._chunks
        self._chunks = []
        return iter(chunks)

    def chunks_from_lines(self, lines: Iterable[str]) -> Iterator[List[str]]:
        if self._current_chunk:
            raise RuntimeError("Current chunk is not empty")

        if self._chunks:
            raise RuntimeError("There are pending chunks")

        self.add_lines(lines)
        self.flush()
        return iter(self)
