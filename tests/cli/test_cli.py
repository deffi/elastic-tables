from pathlib import Path
import subprocess
import sys
import unittest

from elastic_tabs.cli import cli
from data import test_cases


class CliTest(unittest.TestCase):
    """We use text for the output so we get a better diff in the IDE.
    """

    def test_file(self):
        for prefix, input_path, expected_text in test_cases():
            with self.subTest(prefix):
                output = subprocess.check_output([sys.executable, cli.__file__, input_path], text=True)
                self.assertEqual(expected_text, output)

    def test_stdin(self):
        args = [sys.executable, cli.__file__]
        for prefix, input_path, expected_text in test_cases():
            with self.subTest(prefix):
                # Pass the input as text because the text parameter applies to both
                # input and output
                output = subprocess.check_output(args, input=input_path.read_text(), text=True)
                self.assertEqual(expected_text, output)

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if __name__ == '__main__':
    unittest.main()
