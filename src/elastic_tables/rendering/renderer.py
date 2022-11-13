import re
from typing import Sequence, Iterator, Callable

from elastic_tables.model import Table, Row

numeric_pattern = re.compile(r'\s*[+-]?\d+\s*')


class Renderer:
    def __init__(self):
        self.align_numeric = False

    def render(self, table: Table) -> Iterator[str]:
        columns_widths = table.column_widths()

        if self.align_numeric:
            column_is_numeric = table.columns_match(numeric_pattern)
            default_columns_alignment = [str.rjust if numeric else str.ljust for numeric in column_is_numeric]
        else:
            default_columns_alignment = [str.ljust] * len(columns_widths)

        return (row.render(columns_widths, default_columns_alignment) for row in table.rows)
