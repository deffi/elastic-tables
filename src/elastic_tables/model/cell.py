from __future__ import annotations
from typing import Optional, Callable

from dataclasses import dataclass

AlignmentFunction = Callable[[str, int], str]


@dataclass(frozen=True)
class Cell:
    text: str
    alignment: Optional[AlignmentFunction] = None

    def render(self, width: int, default_alignment: Optional[AlignmentFunction]) -> str:
        if len(self.text) > width:
            raise ValueError(f"Text too long for width {width}: {self.text}")

        alignment = self.alignment or default_alignment or str.ljust
        return alignment(self.text, width)

    def __len__(self):
        return len(self.text)
