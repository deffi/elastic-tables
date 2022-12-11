import unittest

from elastic_tables.model import Cell
from elastic_tables.filter import Filter
from elastic_tables.util.alignment import left, right, center


class FilterTest(unittest.TestCase):
    def test_splitting(self):
        f = Filter()

        f.input("foo\tb\n")
        self.assertEqual("", f.text(clear=False))
        f.input("b\tbar\v\n")
        self.assertEqual("foob\nb  bar\n", f.text())

    def test_flush(self):
        f = Filter()

        f.input("foo\tb\n")
        self.assertEqual("", f.text(clear=False))
        f.flush()
        self.assertEqual("foob\n", f.text())

    def test_align_cell_space(self):
        # Basic alignment
        self.assertEqual(Cell("foo", None), Filter.align_cell_space(Cell("foo", None)))
        self.assertEqual(Cell("foo", left), Filter.align_cell_space(Cell("foo ", None)))
        self.assertEqual(Cell("foo", right), Filter.align_cell_space(Cell(" foo", None)))
        self.assertEqual(Cell("foo", center), Filter.align_cell_space(Cell(" foo ", None)))

        # Blank cells
        self.assertEqual(Cell(" " * 0, None), Filter.align_cell_space(Cell(" " * 0, None)))
        self.assertEqual(Cell(" " * 0, None), Filter.align_cell_space(Cell(" " * 1, None)))
        self.assertEqual(Cell(" " * 0, None), Filter.align_cell_space(Cell(" " * 2, None)))
        self.assertEqual(Cell(" " * 1, None), Filter.align_cell_space(Cell(" " * 3, None)))
        self.assertEqual(Cell(" " * 2, None), Filter.align_cell_space(Cell(" " * 4, None)))

    def test_filter(self):
        self.assertEqual("foob\nb  bar", Filter.filter("foo\tb\nb\tbar"))


if __name__ == '__main__':
    unittest.main()
