from typing import Optional

from elastic_tables.filter import Filter

import data as test_data


class TestFilter:
    def _test(self, subtests, prefix: str, filter_args: dict = None, suffix: Optional[str] = "", *,
              column_separator: Optional[str] = "|"):
        if filter_args is None:
            filter_args = {}

        if column_separator is not None:
            filter_args["column_separator"] = column_separator

        input_, expected = test_data.test_case_data(prefix, suffix)

        with subtests.test(prefix=prefix, suffix=suffix, filter_args=filter_args):
            assert "".join(Filter.filter(input_, **filter_args)) == expected

    def test_column_separator(self, subtests):
        self._test(subtests, "column-separator_tab", column_separator="\t")  # Explicit tab
        self._test(subtests, "column-separator_pipe", column_separator="|")  # Explicit pipe
        self._test(subtests, "column-separator_tab", column_separator=None)  # The filter defaults to tab
        self._test(subtests, "column-separator_pipe")  # This test defaults to pipe

    def test_line_break(self, subtests):
        self._test(subtests, "line-break_lf")  # LF
        self._test(subtests, "line-break_crlf")  # CR/LF

    def test_align_numeric(self, subtests):
        self._test(subtests, "align-numeric", {"align_numeric": True}, "yes")  # Explicit true
        self._test(subtests, "align-numeric", {"align_numeric": False}, "no")  # Explicit false
        self._test(subtests, "align-numeric", {}, "no")  # The filter defaults to false

    def test_align_space(self, subtests):
        self._test(subtests, "align-space", {"align_space": True}, "yes")  # Explicit true
        self._test(subtests, "align-space", {"align_space": False}, "no")  # Explicit false
        self._test(subtests, "align-space", {}, "no")  # The filter defaults to false
