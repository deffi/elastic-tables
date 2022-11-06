from typing import Sequence, Iterator

from elastic_tables.model import Table, Row


class Renderer:
    def __init__(self):
        ...

    def render_cell(self, text: str, width: int) -> str:
        if len(text) > width:
            raise ValueError("Text too long")

        return text.ljust(width)

    def render_row(self, row: Row, widths: Sequence[int]) -> str:
        rendered_cells = (self.render_cell(cell, width) for cell, width in zip (row.cells, widths))
        return "".join(rendered_cells) + row.line_terminator

    def render(self, table: Table) -> Iterator[str]:
        columns_widths = table.column_widths()
        return (self.render_row(row, columns_widths) for row in table.rows)
