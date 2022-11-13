import unittest

from elastic_tables.model import Table, Row, Cell, Block, Line, Column


class RenderTest(unittest.TestCase):
    def test_column_alignment(self):
        _ = Cell("")

        # No rows
        self.assertEqual([], Table([]).column_alignment)

        # Single row with varying number of cells
        self.assertEqual([], Table([Row([], "\n")]).column_alignment)
        self.assertEqual([None], Table([Row([_], "\n")]).column_alignment)
        self.assertEqual([None, None], Table([Row([_, _], "\n")]).column_alignment)

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

    def test_column_count(self):
        _ = Cell("")

        # No rows
        self.assertEqual(0, Table([]).column_count())

        # Rows with no cells each
        self.assertEqual(0, Table([Row([], "\n")]).column_count())
        self.assertEqual(0, Table([Row([], "\n"), Row([], "\n")]).column_count())

        # Single row
        self.assertEqual(1, Table([Row([_], "\n")]).column_count())

        # Multiple rows (different number of cells)
        self.assertEqual(2, Table([Row([_, _], "\n"), Row([_], "\n")]).column_count())

    def test_columns(self):
        a = Cell("a")
        b = Cell("b")
        c = Cell("c")
        _ = Cell("")

        # No rows
        self.assertEqual([], list(Table([]).columns()))

        # Rows with no cells each
        self.assertEqual([], list(Table([Row([], "\n")]).columns()))
        self.assertEqual([], list(Table([Row([], "\n"), Row([], "\n")]).columns()))

        # Single row
        self.assertEqual([Column([a])], list(Table([Row([a], "\n")]).columns()))

        # Multiple rows (different number of cells)
        self.assertEqual([Column([a, c]), Column([b, _])], list(Table([Row([a, b], "\n"), Row([c], "\n")]).columns()))

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
