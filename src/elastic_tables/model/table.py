from dataclasses import dataclass
from itertools import zip_longest
from typing import Sequence, Iterator, Pattern

from elastic_tables.model import Row, Cell


@dataclass()
class Table:
    rows: Sequence[Row]

    def columns(self) -> Iterator[Sequence[Cell]]:
        return zip_longest(*(row.cells for row in self.rows), fillvalue=Cell(""))

    @staticmethod
    def column_width(column: Sequence[Cell]) -> int:
        if column:
            return max(len(cell) for cell in column)
        else:
            return 0

    @staticmethod
    def column_matches(column: Sequence[Cell], pattern: Pattern) -> bool:
        return all(pattern.fullmatch(cell.text) for cell in column)

    def column_widths(self) -> Sequence[int]:
        columns = self.columns()
        return [self.column_width(column) for column in columns]

    def columns_match(self, pattern: Pattern) -> Sequence[bool]:
        columns = self.columns()
        return [self.column_matches(column, pattern) for column in columns]
