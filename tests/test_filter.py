import unittest

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


if __name__ == '__main__':
    unittest.main()
