import unittest

from elastic_tables.model import Line
from elastic_tables.parsing import LineSplitter


foo = Line("foo", "\n")
bar_baz = Line("barbaz", "\n")
qux = Line("qux", "")


class LineSplitterTest(unittest.TestCase):
    def test_simple(self):
        splitter = LineSplitter(None)

        splitter.input("foo\n")
        self.assertEqual([foo], splitter.lines(clear=False))
        self.assertEqual([foo], splitter.lines())
        self.assertEqual([], splitter.lines())

        splitter.input("foo\n")
        self.assertEqual([foo], splitter.lines(clear=False))
        self.assertEqual([foo], splitter.lines())
        self.assertEqual([], splitter.lines())

    def test_multiple(self):
        splitter = LineSplitter(None)
        self.assertEqual([], splitter.lines(clear=False))

        splitter.input("foo\n")
        self.assertEqual([foo], splitter.lines(clear=False))

        splitter.input("bar")
        self.assertEqual([foo], splitter.lines(clear=False))

        splitter.input("baz\n")
        self.assertEqual([foo, bar_baz], splitter.lines(clear=False))

        splitter.input("qux")
        self.assertEqual([foo, bar_baz], splitter.lines(clear=False))

        splitter.flush()
        self.assertEqual([foo, bar_baz, qux], splitter.lines(clear=False))
        self.assertEqual([foo, bar_baz, qux], splitter.lines())
        self.assertEqual([], splitter.lines())

    def test_flush(self):
        splitter = LineSplitter()
        self.assertEqual([], splitter.lines())

        splitter.flush()
        self.assertEqual([], splitter.lines())

        splitter.flush()
        splitter.flush()
        self.assertEqual([], splitter.lines())


if __name__ == '__main__':
    unittest.main()
