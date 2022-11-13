from dataclasses import dataclass
from typing import Sequence, Pattern

from elastic_tables.model import Cell


@dataclass(frozen=True)
class Column:
    cells: Sequence[Cell]

    def width(self) -> int:
        if self.cells:
            return max(len(cell) for cell in self.cells)
        else:
            return 0

    def matches(self, pattern: Pattern) -> bool:
        return all(pattern.fullmatch(cell.text) for cell in self.cells)
