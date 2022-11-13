from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from elastic_tables.model import Line, Cell, AlignmentFunction


@dataclass(frozen=True)
class Row:
    cells: Sequence[Cell]
    line_terminator: str

    @classmethod
    def from_line(cls, line: Line) -> Row:
        cells = [Cell(text) for text in line.content.split("\t")]
        return cls(cells, line.terminator)

    def render(self, widths: Sequence[int], alignments: Sequence[AlignmentFunction]) -> str:
        cell_width_alignment = zip(self.cells, widths, alignments)
        rendered_cells = (cell.render(width, alignment) for cell, width, alignment in cell_width_alignment)
        return "".join(rendered_cells) + self.line_terminator
