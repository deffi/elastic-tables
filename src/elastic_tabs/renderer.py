from elastic_tabs.model import Table

from typing import Sequence, Iterator


class Renderer:
    def __init__(self):
        ...

    def render_cell(self, text: str, width: int) -> str:
        if len(text) > width:
            raise ValueError("Text too long")

        return text.ljust(width)

    def render_row(self, row: Sequence[str], widths: Sequence[int]) -> str:
        return "".join(self.render_cell(cell, width) for cell, width in zip (row, widths))

    def render(self, table: Table) -> Iterator[str]:
        columns_widths = table.column_widths()
        return (self.render_row(row, columns_widths) for row in table.rows)
