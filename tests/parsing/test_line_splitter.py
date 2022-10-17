import unittest

from elastic_tabs.model import Line
from elastic_tabs.parsing import LineSplitter


class LineSplitterTest(unittest.TestCase):
    def test_with_enqueue(self):
        foo = Line("foo", "\n")
        bar_baz = Line("barbaz", "\n")
        qux = Line("qux", "")

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


if __name__ == '__main__':
    unittest.main()
