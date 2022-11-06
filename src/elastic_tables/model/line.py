from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    content: str
    terminator: str
