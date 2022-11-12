import unittest

from elastic_tables.model import Table, Row, Cell
from elastic_tables.rendering import Renderer


class RendererTest(unittest.TestCase):
    def test_render_row(self):
        l = str.ljust
        r = str.rjust
        self.assertEqual("a  foo  bc  \n", Renderer().render_row(Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n"), [3, 5, 1, 3], [l, l, l, l]))
        self.assertEqual("a    foobc  \n", Renderer().render_row(Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n"), [3, 5, 1, 3], [l, r, l, l]))
        self.assertEqual("  a  foob  c\n", Renderer().render_row(Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n"), [3, 5, 1, 3], [r, r, r, r]))

    def test_render_table(self):
        # Empty table
        self.assertEqual([], list(Renderer().render(Table([]))))

        # Empty rows
        self.assertEqual(["\n", "\n"], list(Renderer().render(Table([Row([], "\n"), Row([], "\n")]))))

        # Equal column lengths
        self.assertEqual([
            "foob  \n",  # TODO trailing tabs, yay or nay?
            "b  bar\n"],
            list(Renderer().render(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("b"), Cell("bar")], "\n")]))))

        # Different column lengths
        self.assertEqual([
            "foob\n",
            "f  \n"],  # TODO extra space for second column, yay or nay?
            list(Renderer().render(Table([
                Row([Cell("foo"), Cell("b")], "\n"),
                Row([Cell("f")], "\n")]))))

    def test_align_numeric(self):
        table = Table([
            Row([Cell("a"  ), Cell("+1" ), Cell("222")], "\n"),
            Row([Cell("bb" ), Cell("333"), Cell("44" )], "\n"),
            Row([Cell("ccc"), Cell("55" ), Cell("d"  )], "\n"),
        ])

        renderer = Renderer()
        self.assertEqual(["a  +1 222\n", "bb 33344 \n", "ccc55 d  \n"], list(renderer.render(table)))
        renderer.align_numeric = True
        self.assertEqual(["a   +1222\n", "bb 33344 \n", "ccc 55d  \n"], list(renderer.render(table)))



if __name__ == '__main__':
    unittest.main()
