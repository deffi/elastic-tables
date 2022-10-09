import unittest

from elastic_tabs import Line
from elastic_tabs.text import splitlines, split_lines


class TextTest(unittest.TestCase):
    def test_keep_ends_false(self):
        self.assertEqual(([], ""), splitlines(""))
        self.assertEqual(([""], ""), splitlines("\n"))
        self.assertEqual((["foo", "bar"], ""), splitlines("foo\nbar\n"))
        self.assertEqual((["foo"], "bar"), splitlines("foo\nbar"))
        self.assertEqual((["foo", "", "bar"], ""), splitlines("foo\n\nbar\n"))

    def test_keep_ends_true(self):
        self.assertEqual(([], ""), splitlines("", keep_ends=True))
        self.assertEqual((["\n"], ""), splitlines("\n", keep_ends=True))
        self.assertEqual((["foo\n", "bar\n"], ""), splitlines("foo\nbar\n", keep_ends=True))
        self.assertEqual((["foo\n"], "bar"), splitlines("foo\nbar", keep_ends=True))
        self.assertEqual((["foo\n", "\n", "bar\n"], ""), splitlines("foo\n\nbar\n", keep_ends=True))

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
