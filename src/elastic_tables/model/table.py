from dataclasses import dataclass
from itertools import zip_longest
import re
from typing import Sequence, Iterator, Pattern

from elastic_tables.model import Row, Cell


numeric_pattern = re.compile(r'\s*[+-]?\d+\s*')


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

    def render(self, align_numeric: bool = False) -> Iterator[str]:
        columns_widths = self.column_widths()

        if align_numeric:
            column_is_numeric = self.columns_match(numeric_pattern)
            default_columns_alignment = [str.rjust if numeric else str.ljust for numeric in column_is_numeric]
        else:
            default_columns_alignment = [str.ljust] * len(columns_widths)

        return (row.render(columns_widths, default_columns_alignment) for row in self.rows)
