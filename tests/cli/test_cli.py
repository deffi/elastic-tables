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
        for input_path in self.test_data_path.glob("*_in.txt"):
            prefix = input_path.stem.removesuffix("_in")
            with self.subTest(prefix):
                expected_path = input_path.with_stem(f"{prefix}_expected")
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
