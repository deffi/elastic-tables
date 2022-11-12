import unittest

from elastic_tables.filter import Filter

import data as test_data


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

    def _test_filter_file(self, prefix: str):
        input_path, expected_path = test_data.test_case(prefix)

        input_ = input_path.read_text()
        expected = expected_path.read_text()

        self.assertEqual(expected, "".join(Filter.filter(input_)))

    def test_filter_file(self):
        self._test_filter_file("line-break_lf")
        self._test_filter_file("line-break_crlf")


if __name__ == '__main__':
    unittest.main()
