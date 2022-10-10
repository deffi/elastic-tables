from dataclasses import dataclass
from itertools import zip_longest
from typing import Sequence, Iterator


@dataclass()
class Table:
    rows: Sequence[Sequence[str]]

    def columns(self) -> Iterator[Sequence[str]]:
        return zip_longest(*self.rows, fillvalue="")

    @staticmethod
    def column_width(column: Sequence[str]) -> int:
        if column:
            return max(len(cell) for cell in column)
        else:
            return 0

    def column_widths(self) -> Sequence[int]:
        columns = self.columns()
        return [self.column_width(column) for column in columns]
