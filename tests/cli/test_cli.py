from pathlib import Path
import subprocess
import sys
from typing import Optional, List
import unittest

from elastic_tables.cli import cli
import data as test_data


class CliTest(unittest.TestCase):
    def _test_file(self, input_path: Path, expected_path: Path, args: List[str]):
        output = subprocess.check_output([sys.executable, cli.__file__] + args + [str(input_path)])
        expected = expected_path.read_bytes()
        self.assertEqual(expected, output)

    def _test_stdin(self, input_path: Path, expected_path: Path, args: List[str]):
        input_ = input_path.read_bytes()
        output = subprocess.check_output([sys.executable, cli.__file__] + args, input=input_)
        expected = expected_path.read_bytes()
        self.assertEqual(expected, output)

    def _test(self, prefix: str, args: Optional[List[str]] = None, suffix: Optional[str] = "", *,
              column_separator: Optional[str] = "|"):
        if args is None:
            args = []

        if column_separator is not None:
            args = ["--column-separator", column_separator] + args

        with self.subTest(prefix=prefix, suffix=suffix, args=args):
            input_path, expected_path = test_data.test_case(prefix, suffix)

            with self.subTest(method="file"):
                self._test_file(input_path, expected_path, args)

            with self.subTest(method="stdin"):
                self._test_stdin(input_path, expected_path, args)

    def test_column_separator(self):
        self._test("column-separator_tab", column_separator="\t")  # Explicit tab
        self._test("column-separator_pipe", column_separator="|")  # Explicit pipe
        self._test("column-separator_tab", column_separator=None)  # The CLI defaults to tab
        self._test("column-separator_pipe")  # This test defaults to pipe

    def test_line_break(self):
        self._test("line-break_lf")  # LF
        self._test("line-break_crlf")  # CR/LF

    def test_align_numeric(self):
        self._test("align-numeric", ["--align-numeric"], "yes")  # Explicit true
        self._test("align-numeric", ["--no-align-numeric"], "no")  # Explicit false
        self._test("align-numeric", [], "yes")  # The CLI defaults to true TODO don't use True as default

    def test_align_space(self):
        self._test("align-space", ["--align-space"], "yes")  # Explicit true
        self._test("align-space", ["--no-align-space"], "no")  # Explicit false
        self._test("align-space", [], "yes")  # The CLI defaults to true TODO don't use True as default

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if __name__ == '__main__':
    unittest.main()
