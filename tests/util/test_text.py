import unittest

from elastic_tables.model import Line
from elastic_tables.util.text import split_lines


class TextTest(unittest.TestCase):
    def test_split_lines(self):
        def expand(lines, remainder): return list(lines), remainder

        # Blank line, unterminated (empty string)
        self.assertEqual(([], ""),
                         expand(*split_lines("")))

        # Blank line, terminated
        self.assertEqual(([Line("", "\n")], ""),
                         expand(*split_lines("\n")))

        # Single line, unterminated
        self.assertEqual(([], "foo"),
                         expand(*split_lines("foo")))

        # Single line, terminated
        self.assertEqual(([Line("foo", "\n")], ""),
                         expand(*split_lines("foo\n")))

        # Multiple lines, last unterminated
        self.assertEqual(([Line("foo", "\n")], "bar"),
                         expand(*split_lines("foo\nbar")))

        # Multiple lines, all terminated
        self.assertEqual(([Line("foo", "\n"),
                           Line("bar", "\n")], ""),
                         expand(*split_lines("foo\nbar\n")))

        # Different terminators
        self.assertEqual(([Line("foo", "\r\n"),
                           Line("bar", "\n")], ""),
                         expand(*split_lines("foo\r\nbar\n")))


if __name__ == '__main__':
    unittest.main()
