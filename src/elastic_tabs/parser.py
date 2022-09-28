from typing import Iterator, Iterable, List, Sequence

from elastic_tabs import Table


class Parser:
    def __init__(self):
        pass

    @staticmethod
    def chunks_from_lines(lines: Iterable[str]) -> Iterator[Sequence[str]]:
        rows: List[str] = []

        for line in lines:
            rows.append(line)
            if len(line.strip()) == 0:
                yield rows
                rows = []

        yield rows

    def split_tables(self, lines: Iterable[str]) -> Iterator[Table]:
        for chunk in self.chunks_from_lines(lines):
            yield Table([line.split("\t") for line in chunk])
