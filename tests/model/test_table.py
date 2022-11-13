import re
import unittest

from elastic_tables.model import Table, Row, Cell, Block, Line


class RenderTest(unittest.TestCase):
    def test_from_block(self):
        # Empty
        self.assertEqual(Table([]), Table.from_block(Block([])))

        # Blank
        self.assertEqual(Table([Row([Cell("")], "")]), Table.from_block(Block([
            Line("", ""),
        ])))

        block = Block([
            Line("foo\tb", "\n"),
            Line("or", "\n"),
            Line("f\tbar", "\n"),
        ])

        expected = Table([
            Row([Cell("foo"), Cell("b")], "\n"),
            Row([Cell("or")], "\n"),
            Row([Cell("f"), Cell("bar")], "\n"),
        ])

        self.assertEqual(expected, Table.from_block(block))

    def test_column_width(self):
        self.assertEqual(0, Table.column_width([]))
        self.assertEqual(0, Table.column_width([Cell("")]))
        self.assertEqual(0, Table.column_width([Cell(""), Cell(""), Cell("")]))
        self.assertEqual(1, Table.column_width([Cell("a")]))
        self.assertEqual(3, Table.column_width([Cell("a"), Cell("aaa"), Cell(""), Cell("aa")]))

    def test_column_widths(self):
        # No rows
        self.assertEqual([], Table([]).column_widths())

        # Rows with no cells each
        self.assertEqual([], Table([Row([], "\n")]).column_widths())
        self.assertEqual([], Table([Row([], "\n"), Row([], "\n")]).column_widths())

        # Single row
        self.assertEqual([1], Table([Row([Cell("a")], "\n")]).column_widths())

        # Multiple rows (different number of cells)
        self.assertEqual([3, 2], Table([Row([Cell("a"), Cell("bb")], "\n"), Row([Cell("ccc")], "\n")]).column_widths())

    def test_columns_match(self):
        table = Table([
            Row([Cell("a"),  Cell("1"),  Cell("1")], "\n"),
            Row([Cell("aa"), Cell("11"), Cell("a")], "\n"),
        ])

        numeric = re.compile(r'\d+')
        self.assertEqual([False, True, False], table.columns_match(numeric))

    def test_render(self):
        # Empty table
        self.assertEqual([], list(Table([]).render()))

        # Empty rows
        self.assertEqual(["\n", "\n"], list(Table([Row([], "\n"), Row([], "\n")]).render()))

        # Equal column lengths
        self.assertEqual([
            "foob  \n",  # TODO trailing tabs, yay or nay?
            "b  bar\n"],
            list(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("b"), Cell("bar")], "\n")]).render()))

        # Different column lengths
        self.assertEqual([
            "foob\n",
            "f  \n"],  # TODO extra space for second column, yay or nay?
            list(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("f")], "\n")]).render()))

    def test_align_numeric(self):
        table = Table([
            Row([Cell("a"  ), Cell("+1" ), Cell("222")], "\n"),
            Row([Cell("bb" ), Cell("333"), Cell("44" )], "\n"),
            Row([Cell("ccc"), Cell("55" ), Cell("d"  )], "\n"),
        ])

        self.assertEqual(["a  +1 222\n", "bb 33344 \n", "ccc55 d  \n"], list(table.render(False)))
        self.assertEqual(["a   +1222\n", "bb 33344 \n", "ccc 55d  \n"], list(table.render(True)))


if __name__ == '__main__':
    unittest.main()
