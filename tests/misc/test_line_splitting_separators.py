from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO, BytesIO
import re
from typing import List


# When using str.splitlines and bytes.splitlines, we keep line breaks for
# consistency with StringIO, where we don't have a choice. Also, it's what we'll
# need for the application at hand.

class TestLineSplittingSeparators:
    def test_separators_str(self):
        def split(string: str) -> List[str]:
            return string.splitlines(keepends=True)

        # Strings split on a whole lot of separators
        assert split("foo\nbar")     == ["foo\n"    , "bar"]  # Line feed
        assert split("foo\rbar")     == ["foo\r"    , "bar"]  # Carriage return
        assert split("foo\r\nbar")   == ["foo\r\n"  , "bar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\v"    , "bar"]  # Vertical tab
        assert split("foo\fbar")     == ["foo\f"    , "bar"]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1c"  , "bar"]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1d"  , "bar"]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1e"  , "bar"]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85"  , "bar"]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028", "bar"]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029", "bar"]  # Paragraph separator

    def test_separators_bytes(self):
        def split(byte_string: bytes) -> List[bytes]:
            return byte_string.splitlines(keepends=True)

        # Byte strings only split on CR, LF, and CRLF. Also, there is no unicode
        # in byte strings, so line separator and paragraph separator aren't
        # applicable.
        assert split(b"foo\nbar")   == [b"foo\n"  , b"bar"]  # Line feed
        assert split(b"foo\rbar")   == [b"foo\r"  , b"bar"]  # Carriage return
        assert split(b"foo\r\nbar") == [b"foo\r\n", b"bar"]  # Carriage return + line feed
        assert split(b"foo\vbar")   == [b"foo\vbar"  ]       # Vertical tab
        assert split(b"foo\fbar")   == [b"foo\fbar"  ]       # Form feed
        assert split(b"foo\x1cbar") == [b"foo\x1cbar"]       # File separator
        assert split(b"foo\x1dbar") == [b"foo\x1dbar"]       # Group separator
        assert split(b"foo\x1ebar") == [b"foo\x1ebar"]       # Record separator
        assert split(b"foo\x85bar") == [b"foo\x85bar"]       # Next line (C1)
        # No unicode here

    def test_separators_string_io(self):
        def split(string: str) -> List[str]:
            assert StringIO(string).readlines() == list(StringIO(string))
            return list(StringIO(string))

        # StringIO only splits on LF. It looks like it also splits on CRLF, but
        # that's just the split on LF.
        assert split("foo\nbar")     == ["foo\n"  , "bar"]  # Line feed
        assert split("foo\rbar")     == ["foo\rbar"]        # Carriage return
        assert split("foo\r\nbar")   == ["foo\r\n", "bar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\vbar"      ]  # Vertical tab
        assert split("foo\fbar")     == ["foo\fbar"      ]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1cbar"    ]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1dbar"    ]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1ebar"    ]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85bar"    ]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028bar"  ]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029bar"  ]  # Paragraph separator

    def test_separators_bytes_io(self):
        def split(byte_string: bytes) -> List[bytes]:
            assert BytesIO(byte_string).readlines() == list(BytesIO(byte_string))
            return list(BytesIO(byte_string))

        # BytesIO only splits on LF. It looks like it also splits on CRLF, but
        # that's just the split on LF. Also, there is no unicode in byte
        # strings, so line separator and paragraph separator aren't applicable.
        assert split(b"foo\nbar")   == [b"foo\n"  , b"bar"]  # Line feed
        assert split(b"foo\rbar")   == [b"foo\rbar"       ]  # Carriage return
        assert split(b"foo\r\nbar") == [b"foo\r\n", b"bar"]  # Carriage return + line feed
        assert split(b"foo\vbar")   == [b"foo\vbar"       ]  # Vertical tab
        assert split(b"foo\fbar")   == [b"foo\fbar"       ]  # Form feed
        assert split(b"foo\x1cbar") == [b"foo\x1cbar"     ]  # File separator
        assert split(b"foo\x1dbar") == [b"foo\x1dbar"     ]  # Group separator
        assert split(b"foo\x1ebar") == [b"foo\x1ebar"     ]  # Record separator
        assert split(b"foo\x85bar") == [b"foo\x85bar"     ]  # Next line (C1)

    def test_separators_text_file_universal_newlines_translate(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline=None) as file:  # Universal newlines
                    result = list(file)
            return result

        # Input text files (with universal newlines) translate CR, LF, and CRLF
        # to LF and then only split on LF.
        assert split("foo\nbar")     == ["foo\n", "bar"]  # Line feed
        assert split("foo\rbar")     == ["foo\n", "bar"]  # Carriage return
        assert split("foo\r\nbar")   == ["foo\n", "bar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\vbar"    ]  # Vertical tab
        assert split("foo\fbar")     == ["foo\fbar"    ]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1cbar"  ]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1dbar"  ]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1ebar"  ]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85bar"  ]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028bar"]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029bar"]  # Paragraph separator

    def test_separators_text_file_universal_newlines_original(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline='') as file:  # Non-translating universal newlines
                    result = list(file)
            return result

        # Input text files (with non-translating universal newlines) translate CR, LF, and CRLF
        # to LF and then only split on LF.
        assert split("foo\nbar")     == ["foo\n"  , "bar"]  # Line feed
        assert split("foo\rbar")     == ["foo\r"  , "bar"]  # Carriage return
        assert split("foo\r\nbar")   == ["foo\r\n", "bar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\vbar"      ]  # Vertical tab
        assert split("foo\fbar")     == ["foo\fbar"      ]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1cbar"    ]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1dbar"    ]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1ebar"    ]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85bar"    ]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028bar"  ]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029bar"  ]  # Paragraph separator

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
        assert split("foo\nbar")     == ["foo\nbar"      ]  # Line feed
        assert split("foo\rbar")     == ["foo\r", "bar"  ]  # Carriage return
        assert split("foo\r\nbar")   == ["foo\r", "\nbar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\vbar"      ]  # Vertical tab
        assert split("foo\fbar")     == ["foo\fbar"      ]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1cbar"    ]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1dbar"    ]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1ebar"    ]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85bar"    ]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028bar"  ]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029bar"  ]  # Paragraph separator

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
        assert split(b"foo\nbar")   == [b"foo\n"  , b"bar"]  # Line feed
        assert split(b"foo\rbar")   == [b"foo\rbar"       ]  # Carriage return
        assert split(b"foo\r\nbar") == [b"foo\r\n", b"bar"]  # Carriage return + line feed
        assert split(b"foo\vbar")   == [b"foo\vbar"       ]  # Vertical tab
        assert split(b"foo\fbar")   == [b"foo\fbar"       ]  # Form feed
        assert split(b"foo\x1cbar") == [b"foo\x1cbar"     ]  # File separator
        assert split(b"foo\x1dbar") == [b"foo\x1dbar"     ]  # Group separator
        assert split(b"foo\x1ebar") == [b"foo\x1ebar"     ]  # Record separator
        assert split(b"foo\x85bar") == [b"foo\x85bar"     ]  # Next line (C1)

    def test_separators_re(self):
        def grouper(n, iterable, fill_value=None):
            from itertools import zip_longest
            args = [iter(iterable)] * n
            return zip_longest(fillvalue=fill_value, *args)

        def split(string: str) -> List[str]:
            groups = re.split(r'(\n)', string)
            groups.append("")
            result = ["".join(pair) for pair in grouper(2, groups, None)]
            return result

        # This way, we can split on \n ourselves. Since we're including the
        # separator in the result, we get \r\n automatically.
        assert split("foo\nbar")     == ["foo\n"  , "bar"]  # Line feed
        assert split("foo\rbar")     == ["foo\rbar"      ]  # Carriage return
        assert split("foo\r\nbar")   == ["foo\r\n", "bar"]  # Carriage return + line feed
        assert split("foo\vbar")     == ["foo\vbar"      ]  # Vertical tab
        assert split("foo\fbar")     == ["foo\fbar"      ]  # Form feed
        assert split("foo\x1cbar")   == ["foo\x1cbar"    ]  # File separator
        assert split("foo\x1dbar")   == ["foo\x1dbar"    ]  # Group separator
        assert split("foo\x1ebar")   == ["foo\x1ebar"    ]  # Record separator
        assert split("foo\x85bar")   == ["foo\x85bar"    ]  # Next line (C1)
        assert split("foo\u2028bar") == ["foo\u2028bar"  ]  # Line separator
        assert split("foo\u2029bar") == ["foo\u2029bar"  ]  # Paragraph separator




