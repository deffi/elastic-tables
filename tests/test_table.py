import unittest

from elastic_tabs import Table


class RenderTest(unittest.TestCase):
    def test_column_width(self):
        self.assertEqual(0, Table.column_width([]))
        self.assertEqual(0, Table.column_width([""]))
        self.assertEqual(0, Table.column_width(["", "", ""]))
        self.assertEqual(1, Table.column_width(["a"]))
        self.assertEqual(3, Table.column_width(["a", "aaa", "", "aa"]))

    def test_column_widths(self):
        # No rows
        self.assertEqual([], Table([]).column_widths())

        # Rows with no cells each
        self.assertEqual([], Table([[]]).column_widths())
        self.assertEqual([], Table([[], []]).column_widths())

        # Single row
        self.assertEqual([1], Table([["a"]]).column_widths())

        # Multiple rows (different number of cells)
        self.assertEqual([3, 2], Table([["a", "bb"], ["ccc"]]).column_widths())

    def test_render_cell(self):
        # Empty string
        self.assertEqual("", Table.render_cell("", 0))
        self.assertEqual("    ", Table.render_cell("", 4))

        # Pad
        self.assertEqual("foo ", Table.render_cell("foo", 4))

        # Fits
        self.assertEqual("foo", Table.render_cell("foo", 3))

        # Too long
        with self.assertRaises(ValueError):
            Table.render_cell("foobar", 4)

    def test_render_row(self):
        self.assertEqual("a  foo  bc  ", Table.render_row(["a", "foo", "b", "c"], [3, 5, 1, 3]))

    def test_render_table(self):
        # Empty table
        self.assertEqual([], Table([]).render())

        # Empty rows
        self.assertEqual(["", ""], Table([[], []]).render())

        # Equal column lengths
        self.assertEqual([
            "foob  ",  # TODO trailing tabs, yay or nay?
            "b  bar"],
            Table([
                ["foo", "b"],
                ["b", "bar"]]).render())

        # Different column lengths
        self.assertEqual([
            "foob",
            "f  "],  # TODO extra space for second column, yay or nay?
            Table([
                ["foo", "b"],
                ["f"]]).render())


if __name__ == '__main__':
    unittest.main()
