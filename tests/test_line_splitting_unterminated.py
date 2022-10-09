from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO, BytesIO
from typing import List
import unittest


class LineSplittingUnterminatedTests(unittest.TestCase):
    def test_unterminated_str(self):
        def split(string: str) -> List[str]:
            return string.splitlines(keepends=True)

        self.assertEqual([]       , split(""))       # No lines
        self.assertEqual(["\n"]   , split("\n"))     # Single empty line
        self.assertEqual(["foo"]  , split("foo"))    # Single unterminated line
        self.assertEqual(["foo\n"], split("foo\n"))  # Single terminated line

    def test_unterminated_bytes(self):
        def split(byte_string: bytes) -> List[bytes]:
            return byte_string.splitlines(keepends=True)

        self.assertEqual([]        , split(b""))       # No lines
        self.assertEqual([b"\n"]   , split(b"\n"))     # Single empty line
        self.assertEqual([b"foo"]  , split(b"foo"))    # Single unterminated line
        self.assertEqual([b"foo\n"], split(b"foo\n"))  # Single terminated line

    def test_unterminated_string_io(self):
        def split(string: str) -> List[str]:
            self.assertEqual(list(StringIO(string)), StringIO(string).readlines())
            return list(StringIO(string))

        self.assertEqual([]       , split(""))       # No lines
        self.assertEqual(["\n"]   , split("\n"))     # Single empty line
        self.assertEqual(["foo"]  , split("foo"))    # Single unterminated line
        self.assertEqual(["foo\n"], split("foo\n"))  # Single terminated line

    def test_unterminated_bytes_io(self):
        def split(byte_string: bytes) -> List[bytes]:
            self.assertEqual(list(BytesIO(byte_string)), BytesIO(byte_string).readlines())
            return list(BytesIO(byte_string))

        self.assertEqual([]        , split(b""))       # No lines
        self.assertEqual([b"\n"]   , split(b"\n"))     # Single empty line
        self.assertEqual([b"foo"]  , split(b"foo"))    # Single unterminated line
        self.assertEqual([b"foo\n"], split(b"foo\n"))  # Single terminated line

    def test_unterminated_text_file(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline=None) as file:  # Universal newlines
                    result = list(file)
            return result

        self.assertEqual([]       , split(""))       # No lines
        self.assertEqual(["\n"]   , split("\n"))     # Single empty line
        self.assertEqual(["foo"]  , split("foo"))    # Single unterminated line
        self.assertEqual(["foo\n"], split("foo\n"))  # Single terminated line

    def test_unterminated_binary_file(self):
        def split(byte_string: bytes) -> List[bytes]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(byte_string)
                with open(file_path, "rb") as file:
                    result = list(file)
            return result

        self.assertEqual([]        , split(b""))       # No lines
        self.assertEqual([b"\n"]   , split(b"\n"))     # Single empty line
        self.assertEqual([b"foo"]  , split(b"foo"))    # Single unterminated line
        self.assertEqual([b"foo\n"], split(b"foo\n"))  # Single terminated line


if __name__ == '__main__':
    unittest.main()
