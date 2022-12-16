from dataclasses import replace

from elastic_tables.model import Row, Line, Cell
from elastic_tables.util.alignment import left as L, right as R


class TestRow:
    def test_from_line(self):
        assert Row.from_line(Line("foo\tbar", "\n")) == Row([Cell("foo"), Cell("bar")], "\n")

    def test_render(self):
        row = Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n")

        # Without trim
        assert row.render([3, 5, 1, 3], [L, L, L, L], False) == "a  foo  bc  \n"
        assert row.render([3, 5, 1, 3], [L, R, L, L], False) == "a    foobc  \n"
        assert row.render([3, 5, 1, 3], [R, R, R, R], False) == "  a  foob  c\n"

        # With trim
        assert row.render([3, 5, 1, 3], [L, L, L, L], True) == "a  foo  bc\n"
        assert row.render([3, 5, 1, 3], [L, R, L, L], True) == "a    foobc\n"
        assert row.render([3, 5, 1, 3], [R, R, R, R], True) == "  a  foob  c\n"

    def test_map_cells(self):
        def upper(cell: Cell) -> Cell:
            return replace(cell, text=cell.text.upper())

        row = Row([Cell("a"), Cell("foo"), Cell("b")], "\n")
        row = row.map_cells(upper)
        assert row == Row([Cell("A"), Cell("FOO"), Cell("B")], "\n")
