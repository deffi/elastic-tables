import unittest

from elastic_tables.model import Row, Line, Cell


class RowTest(unittest.TestCase):
    def test_from_line(self):
        self.assertEqual(Row([Cell("foo"), Cell("bar")], "\n"), Row.from_line(Line("foo\tbar", "\n")))

    def test_render(self):
        l = str.ljust
        r = str.rjust
        self.assertEqual("a  foo  bc  \n", Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n").render([3, 5, 1, 3], [l, l, l, l]))
        self.assertEqual("a    foobc  \n", Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n").render([3, 5, 1, 3], [l, r, l, l]))
        self.assertEqual("  a  foob  c\n", Row([Cell("a"), Cell("foo"), Cell("b"), Cell("c")], "\n").render([3, 5, 1, 3], [r, r, r, r]))


if __name__ == '__main__':
    unittest.main()
