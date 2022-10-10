from dataclasses import dataclass
from typing import Sequence

from elastic_tabs import Line


@dataclass(frozen=True)
class Block:
    lines: Sequence[Line]
