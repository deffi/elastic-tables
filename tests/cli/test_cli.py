import subprocess
import os
import sys
from typing import List

import pytest

from elastic_tables.cli import cli
import data as test_data


class TestCli:
    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete

    @pytest.mark.parametrize("method", ["file", "stdin"])
    @pytest.mark.parametrize("prefix, args, suffix", [
        # Column separators
        ["column-separator_tab" , ["--column-separator", "\t"], ""],  # Explicit tab
        ["column-separator_pipe", ["--column-separator", "|" ], ""],  # Explicit pipe
        ["column-separator_tab" , ["--column-separator", ... ], ""],  # The CLI defaults to tab
        ["column-separator_pipe", [],                           ""],  # This test defaults to pipe

        # Line breaks
        ["line-break_lf"  , [], ""],  # LF
        ["line-break_crlf", [], ""],  # CR/LF

        # Numeric alignment
        ["align-numeric", ["--align-numeric"   ], "yes"],  # True
        ["align-numeric", ["--no-align-numeric"], "no" ],  # False
        ["align-numeric", []                    , "no" ],  # CLI default: False

        # Space alignment
        ["align-space", ["--align-space"   ], "yes"],  # True
        ["align-space", ["--no-align-space"], "no" ],  # False
        ["align-space", []                  , "no" ],  # CLI default: False
    ], ids=str)
    def test_cli(self, method, prefix: str, args: List[str], suffix: str):
        args = args[::]  # Avoid mutating the argument

        # If column_separator is not specified, use "|" (test default). If it is
        # ..., remove (filter default).
        if "--column-separator" not in args:
            args.extend(["--column-separator", "|"])
        elif args[args.index("--column-separator")+1] is ...:
            args[args.index("--column-separator"):args.index("--column-separator")+2] = []

        input_path, expected_path = test_data.test_case(prefix, suffix)

        if method == "file":
            output = subprocess.check_output([sys.executable, cli.__file__] + args + [str(input_path)])
        elif method == "stdin":
            output = subprocess.check_output([sys.executable, cli.__file__] + args, input=input_path.read_bytes())
        else:
            raise ValueError(f"Unhandled method: {method}")

        expected = expected_path.read_bytes()
        assert output == expected


if os.environ.get("SKIP_CLI_TEST") == "1":
    print("Skipping CLI test")
    CliTest = None
