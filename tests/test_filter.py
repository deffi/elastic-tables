import unittest

from elastic_tabs import Filter


class FilterTest(unittest.TestCase):
    def test_splitting(self):
        f = Filter()

        self.assertEqual([], list(f.add_line("foo\tb")))
        self.assertEqual(["foob  ", "b  bar"], list(f.add_line("b\tbar\v")))

    def test_flush(self):
        f = Filter()

        self.assertEqual([], list(f.add_line("foo\tb")))
        self.assertEqual(["foob"], list(f.flush()))


if __name__ == '__main__':
    unittest.main()
