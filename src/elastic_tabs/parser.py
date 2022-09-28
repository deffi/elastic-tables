from typing import Iterator, Iterable, List, Sequence

from elastic_tabs import Table


class Parser:
    separator = "\t"

    def __init__(self):
        pass

    def chunks_from_lines(self, lines: Iterable[str]) -> Iterator[Sequence[str]]:
        rows: List[str] = []

        for line in lines:
            rows.append(line)
            if len(line.strip()) == 0:
                yield rows
                rows = []

        yield rows

    def row_from_line(self, line: str) -> Iterator[str]:
        return line.split(self.separator)

    def rows_from_lines(self, lines: Iterable[str]) -> Iterator[Sequence[str]]:
        return (list(self.row_from_line(line)) for line in lines)

    def table_from_chunk(self, chunk: Sequence[str]):
        return Table(list(self.rows_from_lines(chunk)))

    def tables_from_chunks(self, chunks: Iterable[Sequence[str]]):
        for chunk in chunks:
            yield self.table_from_chunk(chunk)

    def tables_from_lines(self, lines: Iterable[str]) -> Iterator[Table]:
        return self.tables_from_chunks(self.chunks_from_lines(lines))
