from itertools import zip_longest
from typing import Sequence


def column_width(column: Sequence[str]) -> int:
    if column:
        return max(len(cell) for cell in column)
    else:
        return 0


def column_widths(rows: Sequence[Sequence[str]]) -> Sequence[int]:
    return [column_width(column) for column in zip_longest(*rows, fillvalue="")]


def render_cell(text: str, width: int) -> str:
    if len(text) > width:
        raise ValueError("Text too long")

    return text.ljust(width)


def render_row(row: Sequence[str], widths: Sequence[int]) -> str:
    return "".join(render_cell(cell, width) for cell, width in zip (row, widths))


def render_table(rows: Sequence[Sequence[str]]) -> Sequence[str]:
    columns_widths = column_widths(rows)
    return [render_row(row, columns_widths) for row in rows]
