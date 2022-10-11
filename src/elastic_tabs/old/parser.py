from typing import Iterator, Iterable

from elastic_tabs.model import Table, Row


class Parser:
    separator = "\t"

    def __init__(self):
        pass

    def _row_from_line(self, line: str) -> Iterator[str]:
        return line.split(self.separator)

    def _rows_from_lines(self, lines: Iterable[str]) -> Iterator[Iterator[str]]:
        return (self._row_from_line(line) for line in lines)

    def table_from_chunk(self, chunk: Iterable[str]) -> Table:
        rows = self._rows_from_lines(chunk)
        return Table([Row(list(row), "\n") for row in rows])
