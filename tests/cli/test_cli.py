from typing import Iterator, Tuple
from pathlib import Path
import subprocess
import sys
import unittest


class CliTest(unittest.TestCase):
    """We use text for the output so we get a better diff in the IDE.
    """

    script_path = Path(__file__).parent.parent.parent / "src" / "elastic_tabs" / "cli" / "cli.py"
    test_data_path = Path(__file__).parent.parent / "data"

    def _test_cases(self) -> Iterator[Tuple[Path, str]]:
        """Yields input_path, expected_text"""
        for prefix in ["line-break_crlf", "line-break_lf"]:
            with self.subTest(prefix):
                input_path = self.test_data_path / f"{prefix}_in.txt"
                expected_path = self.test_data_path / f"{prefix}_expected.txt"

                yield input_path, expected_path.read_text()

    def test_file(self):
        for input_path, expected_text in self._test_cases():
            output = subprocess.check_output([sys.executable, self.script_path, input_path], text=True)
            self.assertEqual(expected_text, output)

    def test_stdin(self):
        args = [sys.executable, self.script_path]
        for input_path, expected_text in self._test_cases():
            # Pass the input as text because the text parameter applies to both
            # input and output
            output = subprocess.check_output(args, input=input_path.read_text(), text=True)
            self.assertEqual(expected_text, output)

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if __name__ == '__main__':
    unittest.main()
