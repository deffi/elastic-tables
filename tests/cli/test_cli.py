from pathlib import Path
import subprocess
import sys
import unittest

from tab_les.cli import cli
import data as test_data


class CliTest(unittest.TestCase):
    def _test_file(self, input_path: Path, expected_path: Path):
        output = subprocess.check_output([sys.executable, cli.__file__, input_path])
        expected = expected_path.read_bytes()
        self.assertEqual(expected, output)

    def _test_stdin(self, input_path: Path, expected_path: Path):
        input_ = input_path.read_bytes()
        output = subprocess.check_output([sys.executable, cli.__file__], input=input_)
        expected = expected_path.read_bytes()
        self.assertEqual(expected, output)

    def _test(self, prefix: str):
        with self.subTest(prefix=prefix):
            input_path, expected_path = test_data.test_case(prefix)

            with self.subTest(method="file"):
                self._test_file(input_path, expected_path)

            with self.subTest(method="stdin"):
                self._test_stdin(input_path, expected_path)

    def test_line_break(self):
        self._test("line-break_lf")
        self._test("line-break_crlf")

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if __name__ == '__main__':
    unittest.main()
