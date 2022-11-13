from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Sequence, Callable

from elastic_tables.model import Line, Cell, AlignmentFunction


@dataclass(frozen=True)
class Row:
    cells: Sequence[Cell]
    line_terminator: str

    @classmethod
    def from_line(cls, line: Line, separator: str = "\t") -> Row:
        cells = [Cell(text) for text in line.content.split(separator)]
        return cls(cells, line.terminator)

    def __len__(self):
        return len(self.cells)

    def render(self, widths: Sequence[int], alignments: Sequence[AlignmentFunction]) -> str:
        cell_width_alignment = zip(self.cells, widths, alignments)
        rendered_cells = (cell.render(width, alignment) for cell, width, alignment in cell_width_alignment)
        return "".join(rendered_cells) + self.line_terminator

    def map_cells(self, function: Callable[[Cell], Cell]) -> Row:
        cells = [function(cell) for cell in self.cells]
        return replace(self, cells=cells)
