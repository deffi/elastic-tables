from itertools import zip_longest
from typing import Sequence, Iterator


class Table:
    def __init__(self, rows: Sequence[Sequence[str]]):
        self._rows = rows

    def columns(self) -> Iterator[Sequence[str]]:
        return zip_longest(*self._rows, fillvalue="")

    @staticmethod
    def column_width(column: Sequence[str]) -> int:
        if column:
            return max(len(cell) for cell in column)
        else:
            return 0

    def column_widths(self) -> Sequence[int]:
        columns = self.columns()
        return [self.column_width(column) for column in columns]

    @staticmethod
    def render_cell(text: str, width: int) -> str:
        if len(text) > width:
            raise ValueError("Text too long")

        return text.ljust(width)

    @classmethod
    def render_row(cls, row: Sequence[str], widths: Sequence[int]) -> str:
        return "".join(cls.render_cell(cell, width) for cell, width in zip (row, widths))

    def render(self) -> Sequence[str]:
        columns_widths = self.column_widths()
        return [self.render_row(row, columns_widths) for row in self._rows]
