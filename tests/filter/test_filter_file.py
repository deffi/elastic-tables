import unittest
from typing import Optional

from elastic_tables.model import Cell
from elastic_tables.filter import Filter
from elastic_tables.util.alignment import left, right, center

import data as test_data


class FilterTest(unittest.TestCase):
    def _test(self, prefix: str, filter_args: dict = None, suffix: Optional[str] = "", *,
              column_separator: Optional[str] = "|"):
        if filter_args is None:
            filter_args = {}

        if column_separator is not None:
            filter_args["column_separator"] = column_separator

        input_path, expected_path = test_data.test_case(prefix, suffix)

        input_ = input_path.read_text()
        expected = expected_path.read_text()

        with self.subTest(prefix=prefix, suffix=suffix, filter_args=filter_args):
            self.assertEqual(expected, "".join(Filter.filter(input_, **filter_args)))

    def test_column_separator(self):
        self._test("column-separator_tab", column_separator=None)  # The filter defaults to tab
        self._test("column-separator_tab", column_separator="\t")  # Explicit tab
        self._test("column-separator_pipe", column_separator="|")  # Explicit pipe
        self._test("column-separator_pipe")  # This test defaults to pipe

    def test_line_break(self):
        self._test("line-break_lf")
        self._test("line-break_crlf")

    def test_align_numeric(self):
        self._test("align-numeric", {}, "no")
        self._test("align-numeric", {"align_numeric": True}, "yes")
        self._test("align-numeric", {"align_numeric": False}, "no")

    def test_align_space(self):
        self._test("align-space", {}, "no")
        self._test("align-space", {"align_space": True}, "yes")
        self._test("align-space", {"align_space": False}, "no")


if __name__ == '__main__':
    unittest.main()
