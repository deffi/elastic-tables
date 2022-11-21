from dataclasses import replace
import unittest

from elastic_tables.model import Row, Line, Cell
from elastic_tables.util.alignment import left as L, right as R


class RowTest(unittest.TestCase):
    def test_from_line(self):
        self.assertEqual(Row([Cell("foo"), Cell("bar")], "\n"), Row.from_line(Line("foo\tbar", "\n")))

    def test_render(self):
        row = Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n")

        # Without trim
        self.assertEqual("a  foo  bc  \n", row.render([3, 5, 1, 3], [L, L, L, L], False))
        self.assertEqual("a    foobc  \n", row.render([3, 5, 1, 3], [L, R, L, L], False))
        self.assertEqual("  a  foob  c\n", row.render([3, 5, 1, 3], [R, R, R, R], False))

        # With trim
        self.assertEqual("a  foo  bc\n", row.render([3, 5, 1, 3], [L, L, L, L], True))
        self.assertEqual("a    foobc\n", row.render([3, 5, 1, 3], [L, R, L, L], True))
        self.assertEqual("  a  foob  c\n", row.render([3, 5, 1, 3], [R, R, R, R], True))

    def test_map_cells(self):
        def upper(cell: Cell) -> Cell:
            return replace(cell, text=cell.text.upper())

        row = Row([Cell("a"), Cell("foo"), Cell("b")], "\n")
        row = row.map_cells(upper)
        self.assertEqual(Row([Cell("A"), Cell("FOO"), Cell("B")], "\n"), row)


if __name__ == '__main__':
    unittest.main()
