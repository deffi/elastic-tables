import unittest

from elastic_tables.model import Table, Row
from elastic_tables.rendering import Renderer


class RendererTest(unittest.TestCase):
    def test_render_cell(self):
        # Empty string
        self.assertEqual("", Renderer().render_cell("", 0))
        self.assertEqual("    ", Renderer().render_cell("", 4))

        # Pad
        self.assertEqual("foo ", Renderer().render_cell("foo", 4))

        # Fits
        self.assertEqual("foo", Renderer().render_cell("foo", 3))

        # Too long
        with self.assertRaises(ValueError):
            Renderer().render_cell("foobar", 4)

    def test_render_row(self):
        self.assertEqual("a  foo  bc  \n", Renderer().render_row(Row(["a", "foo", "b", "c"], "\n"), [3, 5, 1, 3]))

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
                Row(["foo", "b"], "\n"),
                Row(["b", "bar"], "\n")]))))

        # Different column lengths
        self.assertEqual([
            "foob\n",
            "f  \n"],  # TODO extra space for second column, yay or nay?
            list(Renderer().render(Table([
                Row(["foo", "b"], "\n"),
                Row(["f"], "\n")]))))


if __name__ == '__main__':
    unittest.main()
