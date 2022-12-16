from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO, BytesIO
from typing import List


class TestLineSplittingUnterminated:
    def test_unterminated_str(self):
        def split(string: str) -> List[str]:
            return string.splitlines(keepends=True)

        assert split("")      == []         # No lines
        assert split("\n")    == ["\n"]     # Single empty line
        assert split("foo")   == ["foo"]    # Single unterminated line
        assert split("foo\n") == ["foo\n"]  # Single terminated line

    def test_unterminated_bytes(self):
        def split(byte_string: bytes) -> List[bytes]:
            return byte_string.splitlines(keepends=True)

        assert split(b"")      == []          # No lines
        assert split(b"\n")    == [b"\n"]     # Single empty line
        assert split(b"foo")   == [b"foo"]    # Single unterminated line
        assert split(b"foo\n") == [b"foo\n"]  # Single terminated line

    def test_unterminated_string_io(self):
        def split(string: str) -> List[str]:
            assert StringIO(string).readlines() == list(StringIO(string))
            return list(StringIO(string))

        assert split("")      == []         # No lines
        assert split("\n")    == ["\n"]     # Single empty line
        assert split("foo")   == ["foo"]    # Single unterminated line
        assert split("foo\n") == ["foo\n"]  # Single terminated line

    def test_unterminated_bytes_io(self):
        def split(byte_string: bytes) -> List[bytes]:
            assert BytesIO(byte_string).readlines() == list(BytesIO(byte_string))
            return list(BytesIO(byte_string))

        assert split(b"")      == []          # No lines
        assert split(b"\n")    == [b"\n"]     # Single empty line
        assert split(b"foo")   == [b"foo"]    # Single unterminated line
        assert split(b"foo\n") == [b"foo\n"]  # Single terminated line

    def test_unterminated_text_file(self):
        def split(string: str) -> List[str]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(string.encode("utf-8"))
                with open(file_path, "r", encoding="utf-8", newline=None) as file:  # Universal newlines
                    result = list(file)
            return result

        assert split("")      == []         # No lines
        assert split("\n")    == ["\n"]     # Single empty line
        assert split("foo")   == ["foo"]    # Single unterminated line
        assert split("foo\n") == ["foo\n"]  # Single terminated line

    def test_unterminated_binary_file(self):
        def split(byte_string: bytes) -> List[bytes]:
            with TemporaryDirectory() as root:
                file_path = Path(root) / "test"
                file_path.write_bytes(byte_string)
                with open(file_path, "rb") as file:
                    result = list(file)
            return result

        assert split(b"")      == []          # No lines
        assert split(b"\n")    == [b"\n"]     # Single empty line
        assert split(b"foo")   == [b"foo"]    # Single unterminated line
        assert split(b"foo\n") == [b"foo\n"]  # Single terminated line
