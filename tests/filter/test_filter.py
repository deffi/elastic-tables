import unittest
from pathlib import Path

from elastic_tabs.filter import Filter

from data import test_cases


class FilterTest(unittest.TestCase):
    def test_splitting(self):
        f = Filter()

        f.input("foo\tb\n")
        self.assertEqual("", f.text(clear=False))
        f.input("b\tbar\v\n")
        self.assertEqual("foob  \nb  bar\n", f.text())

    def test_flush(self):
        f = Filter()

        f.input("foo\tb\n")
        self.assertEqual("", f.text(clear=False))
        f.flush()
        self.assertEqual("foob\n", f.text())

    def test_filter(self):
        self.assertEqual("foob  \nb  bar", Filter.filter("foo\tb\nb\tbar"))

    def test_filter_file(self):
        testdata = Path(__file__).parent.parent / "data"

        for prefix, input_path, expected_text in test_cases():
            with self.subTest(prefix):
                input_ = input_path.read_text()
                expected = expected_text

                self.assertEqual(expected, "".join(Filter.filter(input_)))


if __name__ == '__main__':
    unittest.main()
