import re
from typing import Sequence, Iterator, Callable

from elastic_tables.model import Table, Row



class Renderer:
    def __init__(self):
        self.align_numeric = False

    def render(self, table: Table) -> Iterator[str]:
        return table.render(self.align_numeric)
