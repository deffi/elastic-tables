from elastic_tables.model import Line
from elastic_tables.util.text import split_lines


class TestText:
    def test_split_lines(self):
        def expand(lines, remainder): return list(lines), remainder

        # Blank line, unterminated (empty string)
        assert expand(*split_lines("")) == ([], "")

        # Blank line, terminated
        assert expand(*split_lines("\n")) == ([Line("", "\n")], "")

        # Single line, unterminated
        assert expand(*split_lines("foo")) == ([], "foo")

        # Single line, terminated
        assert expand(*split_lines("foo\n")) == ([Line("foo", "\n")], "")

        # Multiple lines, last unterminated
        assert expand(*split_lines("foo\nbar")) == ([Line("foo", "\n")], "bar")

        # Multiple lines, all terminated
        assert expand(*split_lines("foo\nbar\n")) == ([Line("foo", "\n"), Line("bar", "\n")], "")

        # Different terminators
        assert expand(*split_lines("foo\r\nbar\n")) == ([Line("foo", "\r\n"), Line("bar", "\n")], "")
