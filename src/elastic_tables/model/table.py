from dataclasses import dataclass
from itertools import zip_longest
import re
from typing import Sequence, Iterator, Pattern

from elastic_tables.model import Row, Cell, Block, Column
from elastic_tables.util.alignment import left, right


numeric_pattern = re.compile(r'\s*[+-]?\d+\s*')


@dataclass(frozen=True)
class Table:
    rows: Sequence[Row]

    @classmethod
    def from_block(cls, block: Block, separator: str = "\t"):
        rows = [Row.from_line(line, separator) for line in block.lines]
        return Table(rows)

    def columns(self) -> Iterator[Column]:
        all_cells = zip_longest(*(row.cells for row in self.rows), fillvalue=Cell(""))
        return (Column(list(column_cells)) for column_cells in all_cells)

    def columns_match(self, pattern: Pattern) -> Sequence[bool]:
        columns = self.columns()
        return [column.matches(pattern) for column in columns]

    def render(self, align_numeric: bool = False) -> Iterator[str]:
        column_widths = [column.width() for column in self.columns()]

        if align_numeric:
            column_is_numeric = self.columns_match(numeric_pattern)
            default_columns_alignment = [right if numeric else left for numeric in column_is_numeric]
        else:
            default_columns_alignment = [left] * len(column_widths)

        return (row.render(column_widths, default_columns_alignment) for row in self.rows)
