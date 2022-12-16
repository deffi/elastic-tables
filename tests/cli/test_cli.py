from pathlib import Path
import subprocess
import os
import sys
from typing import Optional, List

from elastic_tables.cli import cli
import data as test_data


class TestCli:
    def _test_file(self, input_path: Path, expected_path: Path, args: List[str]):
        output = subprocess.check_output([sys.executable, cli.__file__] + args + [str(input_path)])
        expected = expected_path.read_bytes()
        assert output == expected

    def _test_stdin(self, input_path: Path, expected_path: Path, args: List[str]):
        input_ = input_path.read_bytes()
        output = subprocess.check_output([sys.executable, cli.__file__] + args, input=input_)
        expected = expected_path.read_bytes()
        assert output == expected

    def _test(self, subtests, prefix: str, args: Optional[List[str]] = None, suffix: Optional[str] = "", *,
              column_separator: Optional[str] = "|"):
        if args is None:
            args = []

        if column_separator is not None:
            args = ["--column-separator", column_separator] + args

        with subtests.test(prefix=prefix, suffix=suffix, args=args):
            input_path, expected_path = test_data.test_case(prefix, suffix)

            with subtests.test(method="file"):
                self._test_file(input_path, expected_path, args)

            with subtests.test(method="stdin"):
                self._test_stdin(input_path, expected_path, args)

    def test_column_separator(self, subtests):
        self._test(subtests, "column-separator_tab", column_separator="\t")  # Explicit tab
        self._test(subtests, "column-separator_pipe", column_separator="|")  # Explicit pipe
        self._test(subtests, "column-separator_tab", column_separator=None)  # The CLI defaults to tab
        self._test(subtests, "column-separator_pipe")  # This test defaults to pipe

    def test_line_break(self, subtests):
        self._test(subtests, "line-break_lf")  # LF
        self._test(subtests, "line-break_crlf")  # CR/LF

    def test_align_numeric(self, subtests):
        self._test(subtests, "align-numeric", ["--align-numeric"], "yes")  # Explicit true
        self._test(subtests, "align-numeric", ["--no-align-numeric"], "no")  # Explicit false
        self._test(subtests, "align-numeric", [], "no")  # The CLI defaults to false

    def test_align_space(self, subtests):
        self._test(subtests, "align-space", ["--align-space"], "yes")  # Explicit true
        self._test(subtests, "align-space", ["--no-align-space"], "no")  # Explicit false
        self._test(subtests, "align-space", [], "no")  # The CLI defaults to false

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if os.environ.get("SKIP_CLI_TEST") == "1":
    print("Skipping CLI test")
    CliTest = None
