from elastic_tables.model import Cell
from elastic_tables.filter import Filter
from elastic_tables.util.alignment import left, right, center


class TestFilter:
    def test_splitting(self):
        f = Filter()

        f.input("foo\tb\n")
        assert f.text(clear=False) == ""
        f.input("b\tbar\v\n")
        assert f.text() == "foob\nb  bar\n"

    def test_flush(self):
        f = Filter()

        f.input("foo\tb\n")
        assert f.text(clear=False) == ""
        f.flush()
        assert f.text() == "foob\n"

    def test_align_cell_space(self):
        # Basic alignment
        assert Filter.align_cell_space(Cell("foo", None)) == Cell("foo", None)
        assert Filter.align_cell_space(Cell("foo ", None)) == Cell("foo", left)
        assert Filter.align_cell_space(Cell(" foo", None)) == Cell("foo", right)
        assert Filter.align_cell_space(Cell(" foo ", None)) == Cell("foo", center)

        # Blank cells
        assert Filter.align_cell_space(Cell(" " * 0, None)) == Cell(" " * 0, None)
        assert Filter.align_cell_space(Cell(" " * 1, None)) == Cell(" " * 0, None)
        assert Filter.align_cell_space(Cell(" " * 2, None)) == Cell(" " * 0, None)
        assert Filter.align_cell_space(Cell(" " * 3, None)) == Cell(" " * 1, None)
        assert Filter.align_cell_space(Cell(" " * 4, None)) == Cell(" " * 2, None)

    def test_filter(self):
        assert Filter.filter("foo\tb\nb\tbar") == "foob\nb  bar"
