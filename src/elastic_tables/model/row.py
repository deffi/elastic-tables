from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from elastic_tables.model import Line, Cell


@dataclass(frozen=True)
class Row:
    cells: Sequence[Cell]
    line_terminator: str

    @classmethod
    def from_line(cls, line: Line) -> Row:
        cells = [Cell(text) for text in line.content.split("\t")]
        return cls(cells, line.terminator)
