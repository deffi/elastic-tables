from typing import Iterator, Iterable, List, Sequence

from elastic_tabs import Table


class Parser:
    def __init__(self):
        pass

    # TODO separate chunk splitting and table generation
    def parse(self, lines: Iterable[str]) -> Iterator[Table]:
        rows: List[Sequence[str]] = []

        def flush() -> Iterator[Table]:
            nonlocal rows
            yield Table(rows)
            rows = []

        for line in lines:
            rows.append(line.split("\t"))
            if len(line.strip()) == 0:
                yield from flush()

        yield from flush()
