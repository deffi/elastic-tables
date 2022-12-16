from dataclasses import replace

from elastic_tables.model import Table, Row, Cell, Block, Line, Column
from elastic_tables.util.alignment import left, right


class TestRender:
    def test_column_alignment(self):
        _ = Cell("")

        # No rows
        assert Table([]).column_alignment == []

        # Single row with varying number of cells
        assert Table([Row([], "\n")]).column_alignment == []
        assert Table([Row([_], "\n")]).column_alignment == [None]
        assert Table([Row([_, _], "\n")]).column_alignment == [None, None]

    def test_from_block(self):
        # Empty
        assert Table.from_block(Block([])) == Table([])

        # Blank
        assert Table.from_block(Block([
            Line("", ""),
        ])) == Table([Row([Cell("")], "")])

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

        assert Table.from_block(block) == expected

    def test_column_count(self):
        _ = Cell("")

        # No rows
        assert Table([]).column_count() == 0

        # Rows with no cells each
        assert Table([Row([], "\n")]).column_count() == 0
        assert Table([Row([], "\n"), Row([], "\n")]).column_count() == 0

        # Single row
        assert Table([Row([_], "\n")]).column_count() == 1

        # Multiple rows (different number of cells)
        assert Table([Row([_, _], "\n"), Row([_], "\n")]).column_count() == 2

    def test_columns(self):
        a = Cell("a")
        b = Cell("b")
        c = Cell("c")
        _ = Cell("")

        # No rows
        assert list(Table([]).columns()) == []

        # Rows with no cells each
        assert list(Table([Row([], "\n")]).columns()) == []
        assert list(Table([Row([], "\n"), Row([], "\n")]).columns()) == []

        # Single row
        assert list(Table([Row([a], "\n")]).columns()) == [Column([a])]

        # Multiple rows (different number of cells)
        assert list(Table([Row([a, b], "\n"), Row([c], "\n")]).columns()) == [Column([a, c]), Column([b, _])]

    def test_render(self):
        # Empty table
        assert list(Table([]).render(False)) == []

        # Empty rows
        assert list(Table([Row([], "\n"), Row([], "\n")]).render(False)) == ["\n", "\n"]

        # Equal column lengths
        assert list(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("b"), Cell("bar")], "\n")]).render(False)) == [
            "foob  \n",  # TODO trailing tabs, yay or nay?
            "b  bar\n"]

        # Different column lengths
        assert list(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("f")], "\n")]).render(False)) == [
            "foob\n",
            "f  \n"]  # TODO extra space for second column, yay or nay?

    def test_numeric_alignment(self):
        table = Table([
            Row([Cell("a"  ), Cell("+1" ), Cell("222")], "\n"),
            Row([Cell("bb" ), Cell("333"), Cell("44" )], "\n"),
            Row([Cell("ccc"), Cell("55" ), Cell("d"  )], "\n"),
        ])

        assert table.numeric_alignment() == [left, right, left]

    def test_align_numeric(self):
        table = Table([
            Row([Cell("a"  ), Cell("+1" ), Cell("222")], "\n"),
            Row([Cell("bb" ), Cell("333"), Cell("44" )], "\n"),
            Row([Cell("ccc"), Cell("55" ), Cell("d"  )], "\n"),
        ])

        assert list(table.render(False)) == ["a  +1 222\n", "bb 33344 \n", "ccc55 d  \n"]
        assert list(table.align_numeric().render(False)) == ["a   +1222\n", "bb 33344 \n", "ccc 55d  \n"]

    def test_map_cells(self):
        def upper(cell: Cell) -> Cell:
            return replace(cell, text=cell.text.upper())

        table = Table([
            Row([Cell("foo"), Cell("bar")], "\n"),
            Row([Cell("baz")], "\n")])

        table = table.map_cells(upper)

        assert table == Table([
            Row([Cell("FOO"), Cell("BAR")], "\n"),
            Row([Cell("BAZ")], "\n")])
