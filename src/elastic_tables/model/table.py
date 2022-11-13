from dataclasses import dataclass, field, replace
from itertools import zip_longest
import re
from typing import Sequence, Iterator, Callable

from elastic_tables.model import Row, Cell, Block, Column, AlignmentFunction
from elastic_tables.util.alignment import left, right


numeric_pattern = re.compile(r'\s*[+-]?\d+\s*')


@dataclass(frozen=True)
class Table:
    rows: Sequence[Row]
    column_alignment: Sequence[AlignmentFunction] = field(default=None)

    def __post_init__(self):
        if self.column_alignment is None:
            object.__setattr__(self, "column_alignment", [None] * self.column_count())

    @classmethod
    def from_block(cls, block: Block, separator: str = "\t"):
        rows = [Row.from_line(line, separator) for line in block.lines]
        return Table(rows)

    def column_count(self) -> int:
        if self.rows:
            return max(len(row) for row in self.rows)
        else:
            return 0

    def columns(self) -> Iterator[Column]:
        all_cells = zip_longest(*(row.cells for row in self.rows), fillvalue=Cell(""))
        return (Column(list(column_cells)) for column_cells in all_cells)

    def render(self) -> Iterator[str]:
        column_widths = [column.width() for column in self.columns()]
        return (row.render(column_widths, self.column_alignment) for row in self.rows)

    #############
    # Transform #
    #############

    def numeric_alignment(self) -> Sequence[AlignmentFunction]:
        column_is_numeric = [column.matches(numeric_pattern) for column in self.columns()]
        return [right if numeric else left for numeric in column_is_numeric]

    def align_numeric(self) -> "Table":
        column_alignment = self.numeric_alignment()
        return replace(self, column_alignment=column_alignment)

    def map_cells(self, function: Callable[[Cell], Cell]) -> "Table":
        rows = [row.map_cells(function) for row in self.rows]
        return replace(self, rows=rows)
