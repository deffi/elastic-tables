import unittest

from elastic_tabs.render import column_width, column_widths, render_cell, render_row, render_table


class RenderTest(unittest.TestCase):
    def test_column_width(self):
        self.assertEqual(0, column_width([]))
        self.assertEqual(0, column_width([""]))
        self.assertEqual(0, column_width(["", "", ""]))
        self.assertEqual(1, column_width(["a"]))
        self.assertEqual(3, column_width(["a", "aaa", "", "aa"]))

    def test_column_widths(self):
        # No rows
        self.assertEqual([], column_widths([]))

        # Rows with no cells each
        self.assertEqual([], column_widths([[]]))
        self.assertEqual([], column_widths([[], []]))

        # Single row
        self.assertEqual([1], column_widths([["a"]]))

        # Multiple rows (different number of cells)
        self.assertEqual([3, 2], column_widths([["a", "bb"], ["ccc"]]))

    def test_render_cell(self):
        # Empty string
        self.assertEqual("", render_cell("", 0))
        self.assertEqual("    ", render_cell("", 4))

        # Pad
        self.assertEqual("foo ", render_cell("foo", 4))

        # Fits
        self.assertEqual("foo", render_cell("foo", 3))

        # Too long
        with self.assertRaises(ValueError):
            render_cell("foobar", 4)

    def test_render_row(self):
        self.assertEqual("a  foo  bc  ", render_row(["a", "foo", "b", "c"], [3, 5, 1, 3]))

    def test_render_table(self):
        # Empty table
        self.assertEqual([], render_table([]))

        # Empty rows
        self.assertEqual(["", ""], render_table([[], []]))

        # Equal column lengths
        self.assertEqual([
            "foob  ",  # TODO trailing tabs, yay or nay?
            "b  bar"],
            render_table([
                ["foo", "b"],
                ["b", "bar"]]))

        # Different column lengths
        self.assertEqual([
            "foob",
            "f  "],  # TODO extra space for second column, yay or nay?
            render_table([
                ["foo", "b"],
                ["f"]]))


if __name__ == '__main__':
    unittest.main()
