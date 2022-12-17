import pytest

from elastic_tables.filter import Filter

import data as test_data


class TestFilter:
    @pytest.mark.parametrize("prefix, filter_args, suffix", [
        # Column separators
        ["column-separator_tab" , {"column_separator": "\t"}, ""],  # Explicit tab
        ["column-separator_pipe", {"column_separator": "|"},  ""],  # Explicit pipe
        ["column-separator_tab" , {"column_separator": ...},  ""],  # The filter defaults to tab
        ["column-separator_pipe", {},                         ""],  # This test defaults to pipe

        # Line breaks
        ["line-break_lf"  , {}, ""],  # LF
        ["line-break_crlf", {}, ""],  # CR/LF

        # Numeric alignment
        ["align-numeric", {"align_numeric": True }, "yes"],  # True
        ["align-numeric", {"align_numeric": False}, "no" ],  # False
        ["align-numeric", {}                      , "no" ],  # Filter default: False

        # Space alignment
        ["align-space", {"align_space": True }, "yes"],  # True
        ["align-space", {"align_space": False}, "no" ],  # False
        ["align-space", {}                    , "no" ],  # Filter default: False
    ], ids=str)
    def test_filter(self, prefix: str, filter_args: dict, suffix: str):
        # If column_separator is not specified, use "|" (test default). If it is
        # ..., remove (filter default).
        if "column_separator" not in filter_args:
            filter_args["column_separator"] = "|"
        elif filter_args["column_separator"] is ...:
            del filter_args["column_separator"]

        input_, expected = test_data.test_case_data(prefix, suffix)
        assert "".join(Filter.filter(input_, **filter_args)) == expected
