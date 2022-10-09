from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO, BytesIO
from typing import List
import unittest


# When using str.splitlines and bytes.splitlines, we keep line breaks for
# consistency with StringIO, where we don't have a choice. Also, it's what we'll
# need for the application at hand.

class LineSplittingSeparatorsTests(unittest.TestCase):
    def test_separators_str(self):
        def split(string: str) -> List[str]:
            return string.splitlines(keepends=True)

        # Strings split on a whole lot of separators
        self.assertEqual(["foo\n"    , "bar"], split("foo\nbar"))      # Line feed
        self.assertEqual(["foo\r"    , "bar"], split("foo\rbar"))      # Carriage return
        self.assertEqual(["foo\r\n"  , "bar"], split("foo\r\nbar"))    # Carriage return + line feed
        self.assertEqual(["foo\v"    , "bar"], split("foo\vbar"))      # Vertical tab
        self.assertEqual(["foo\f"    , "bar"], split("foo\fbar"))      # Form feed
        self.assertEqual(["foo\x1c"  , "bar"], split("foo\x1cbar"))    # File separator
        self.assertEqual(["foo\x1d"  , "bar"], split("foo\x1dbar"))    # Group separator
        self.assertEqual(["foo\x1e"  , "bar"], split("foo\x1ebar"))    # Record separator
        self.assertEqual(["foo\x85"  , "bar"], split("foo\x85bar"))    # Next line (C1)
        self.assertEqual(["foo\u2028", "bar"], split("foo\u2028bar"))  # Line separator
        self.assertEqual(["foo\u2029", "bar"], split("foo\u2029bar"))  # Paragraph separator

    def test_separators_bytes(self):
        def split(byte_string: bytes) -> List[bytes]:
            return byte_string.splitlines(keepends=True)

        # Byte strings only split on CR, LF, and CRLF. Also, there is no unicode
        # in byte strings, so line separator and paragraph separator aren't
        # applicable.
        self.assertEqual([b"foo\n"  , b"bar"], split(b"foo\nbar"))    # Line feed
        self.assertEqual([b"foo\r"  , b"bar"], split(b"foo\rbar"))    # Carriage return
        self.assertEqual([b"foo\r\n", b"bar"], split(b"foo\r\nbar"))  # Carriage return + line feed
        self.assertEqual([b"foo\vbar"  ]     , split(b"foo\vbar"))    # Vertical tab
        self.assertEqual([b"foo\fbar"  ]     , split(b"foo\fbar"))    # Form feed
        self.assertEqual([b"foo\x1cbar"]     , split(b"foo\x1cbar"))  # File separator
        self.assertEqual([b"foo\x1dbar"]     , split(b"foo\x1dbar"))  # Group separator
        self.assertEqual([b"foo\x1ebar"]     , split(b"foo\x1ebar"))  # Record separator
        self.assertEqual([b"foo\x85bar"]     , split(b"foo\x85bar"))  # Next line (C1)
        # No unicode here

    def test_separators_string_io(self):
        def split(string: str) -> List[str]:
            self.assertEqual(list(StringIO(string)), StringIO(string).readlines())
            return list(StringIO(string))

        # StringIO only splits on LF. It looks like it also splits on CRLF, but
        # that's just the split on LF.
        self.assertEqual(["foo\n"  , "bar"], split("foo\nbar"))      # Line feed
        self.assertEqual(["foo\rbar"]      , split("foo\rbar"))      # Carriage return
        self.assertEqual(["foo\r\n", "bar"], split("foo\r\nbar"))    # Carriage return + line feed
        self.assertEqual(["foo\vbar"    ],   split("foo\vbar"))      # Vertical tab
        self.assertEqual(["foo\fbar"    ],   split("foo\fbar"))      # Form feed
        self.assertEqual(["foo\x1cbar"  ],   split("foo\x1cbar"))    # File separator
        self.assertEqual(["foo\x1dbar"  ],   split("foo\x1dbar"))    # Group separator
        self.assertEqual(["foo\x1ebar"  ],   split("foo\x1ebar"))    # Record separator
        self.assertEqual(["foo\x85bar"  ],   split("foo\x85bar"))    # Next line (C1)
        self.assertEqual(["foo\u2028bar"],   split("foo\u2028bar"))  # Line separator
        self.assertEqual(["foo\u2029bar"],   split("foo\u2029bar"))  # Paragraph separator

    def test_separators_bytes_io(self):
        def split(byte_string: bytes) -> List[bytes]:
            self.assertEqual(list(BytesIO(byte_string)), BytesIO(byte_string).readlines())
            return list(BytesIO(byte_string))

        # BytesIO only splits on LF. It looks like it also splits on CRLF, but
        # that's just the split on LF. Also, there is no unicode in byte
        # strings, so line separator and paragraph separator aren't applicable.
        self.assertEqual([b"foo\n"  , b"bar"], split(b"foo\nbar"))      # Line feed
        self.assertEqual([b"foo\rbar"],        split(b"foo\rbar"))      # Carriage return
        self.assertEqual([b"foo\r\n", b"bar"], split(b"foo\r\nbar"))    # Carriage return + line feed
        self.assertEqual([b"foo\vbar"    ],    split(b"foo\vbar"))      # Vertical tab
        self.assertEqual([b"foo\fbar"    ],    split(b"foo\fbar"))      # Form feed
        self.assertEqual([b"foo\x1cbar"  ],    split(b"foo\x1cbar"))    # File separator
        self.assertEqual([b"foo\x1dbar"  ],    split(b"foo\x1dbar"))    # Group separator
        self.assertEqual([b"foo\x1ebar"  ],    split(b"foo\x1ebar"))    # Record separator
        self.assertEqual([b"foo\x85bar"  ],    split(b"foo\x85bar"))    # Next line (C1)

    def test_separators_text_file_universal_newlines(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline=None) as file:  # Universal newlines
                    result = list(file)
            return result

        # Input text files (with universal newlines) translate CR, LF, and CRLF
        # to LF and then only split on LF.
        self.assertEqual(["foo\n", "bar"], split("foo\nbar"))      # Line feed
        self.assertEqual(["foo\n", "bar"], split("foo\rbar"))      # Carriage return
        self.assertEqual(["foo\n", "bar"], split("foo\r\nbar"))    # Carriage return + line feed
        self.assertEqual(["foo\vbar"    ], split("foo\vbar"))      # Vertical tab
        self.assertEqual(["foo\fbar"    ], split("foo\fbar"))      # Form feed
        self.assertEqual(["foo\x1cbar"  ], split("foo\x1cbar"))    # File separator
        self.assertEqual(["foo\x1dbar"  ], split("foo\x1dbar"))    # Group separator
        self.assertEqual(["foo\x1ebar"  ], split("foo\x1ebar"))    # Record separator
        self.assertEqual(["foo\x85bar"  ], split("foo\x85bar"))    # Next line (C1)
        self.assertEqual(["foo\u2028bar"], split("foo\u2028bar"))  # Line separator
        self.assertEqual(["foo\u2029bar"], split("foo\u2029bar"))  # Paragraph separator

    def test_separators_text_file_specific_newlines(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline="\r") as file:  # Universal newlines
                    result = list(file)
            return result

        # Input text files (with universal newlines) translate CR, LF, and CRLF
        # to LF and then only split on LF.
        self.assertEqual(["foo\nbar"], split("foo\nbar"))      # Line feed
        self.assertEqual(["foo\r", "bar"], split("foo\rbar"))      # Carriage return
        self.assertEqual(["foo\r", "\nbar"], split("foo\r\nbar"))    # Carriage return + line feed
        self.assertEqual(["foo\vbar"    ], split("foo\vbar"))      # Vertical tab
        self.assertEqual(["foo\fbar"    ], split("foo\fbar"))      # Form feed
        self.assertEqual(["foo\x1cbar"  ], split("foo\x1cbar"))    # File separator
        self.assertEqual(["foo\x1dbar"  ], split("foo\x1dbar"))    # Group separator
        self.assertEqual(["foo\x1ebar"  ], split("foo\x1ebar"))    # Record separator
        self.assertEqual(["foo\x85bar"  ], split("foo\x85bar"))    # Next line (C1)
        self.assertEqual(["foo\u2028bar"], split("foo\u2028bar"))  # Line separator
        self.assertEqual(["foo\u2029bar"], split("foo\u2029bar"))  # Paragraph separator

    def test_separators_binary_file(self):
        def split(byte_string: bytes) -> List[bytes]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(byte_string)
                with open(file_path, "rb") as file:
                    result = list(file)
            return result

        # Input binary files only split on LF. There is no newlines parameter
        # when opening in binary mode. Also, there is no unicode in binary
        # files, so line separator and paragraph separator aren't applicable.
        self.assertEqual([b"foo\n"  , b"bar"], split(b"foo\nbar"))    # Line feed
        self.assertEqual([b"foo\rbar"       ], split(b"foo\rbar"))    # Carriage return
        self.assertEqual([b"foo\r\n", b"bar"], split(b"foo\r\nbar"))  # Carriage return + line feed
        self.assertEqual([b"foo\vbar"       ], split(b"foo\vbar"))    # Vertical tab
        self.assertEqual([b"foo\fbar"       ], split(b"foo\fbar"))    # Form feed
        self.assertEqual([b"foo\x1cbar"     ], split(b"foo\x1cbar"))  # File separator
        self.assertEqual([b"foo\x1dbar"     ], split(b"foo\x1dbar"))  # Group separator
        self.assertEqual([b"foo\x1ebar"     ], split(b"foo\x1ebar"))  # Record separator
        self.assertEqual([b"foo\x85bar"     ], split(b"foo\x85bar"))  # Next line (C1)

    # def test_str_splitlines_blanks(self):
    #     self.assertEqual([], "".splitlines())            # No lines
    #     self.assertEqual([""], "\n".splitlines())        # Single empty line
    #     self.assertEqual(["foo"], "foo".splitlines())    # Single unterminated line
    #     self.assertEqual(["foo"], "foo\n".splitlines())  # Single terminated line
    #


if __name__ == '__main__':
    unittest.main()
