from pathlib import Path
import subprocess
import sys
import unittest


class CliTest(unittest.TestCase):
    """We use text for the output so we get a better diff in the IDE.
    """

    script_path = Path(__file__).parent.parent.parent / "src" / "elastic_tabs" / "cli" / "cli.py"
    test_data_path = Path(__file__).parent.parent / "data"

    def test_file(self):
        input_path = self.test_data_path / "line-break_crlf_in.txt"
        expected_path = self.test_data_path / "line-break_crlf_expected.txt"

        output = subprocess.check_output([sys.executable, self.script_path, input_path], text=True)
        self.assertEqual(expected_path.read_text(), output)

    def test_stdin(self):
        input_path = self.test_data_path / "line-break_crlf_in.txt"
        expected_path = self.test_data_path / "line-break_crlf_expected.txt"

        # Pass the input as text because the text parameter applies to both
        # input and output
        output = subprocess.check_output([sys.executable, self.script_path], input=input_path.read_text(), text=True)
        self.assertEqual(expected_path.read_text(), output)

    # TODO test that after the first chunk, the first table is output before the
    # second chunk is complete


if __name__ == '__main__':
    unittest.main()
