from dataclasses import dataclass
from typing import Sequence

from elastic_tabs.model import Line


@dataclass(frozen=True)
class Row:
    cells: Sequence[str]
    line_terminator: str

    @classmethod
    def from_line(cls, line: Line):
        return cls(line.content.split("\t"), line.terminator)
