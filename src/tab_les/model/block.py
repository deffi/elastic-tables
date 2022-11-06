from dataclasses import dataclass
from typing import Sequence

from tab_les.model import Line


@dataclass(frozen=True)
class Block:
    lines: Sequence[Line]
