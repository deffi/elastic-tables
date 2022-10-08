import unittest
from pathlib import Path

from elastic_tabs import Filter


class FilterTest(unittest.TestCase):
    def test_splitting(self):
        f = Filter()

        f.add_line("foo\tb")
        self.assertEqual([], list(f.render_tables()))
        f.add_line("b\tbar\v")
        self.assertEqual(["foob  ", "b  bar"], list(f.render_tables()))

    def test_flush(self):
        f = Filter()

        f.add_line("foo\tb")
        self.assertEqual([], list(f.render_tables()))
        f.flush()
        self.assertEqual(["foob"], list(f.render_tables()))

    def test_filter(self):
        self.assertEqual("foob  \nb  bar", Filter.filter("foo\tb\nb\tbar"))

    def test_filter_file(self):
        testdata = Path(__file__).parent / "data"

        self.assertEqual((testdata / "test1_expected.txt").read_text(), Filter.filter((testdata / "test1_in.txt").read_text()))

if __name__ == '__main__':
    unittest.main()
