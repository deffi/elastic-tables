import unittest
from textwrap import dedent

from elastic_tabs.model import Table, Row
from elastic_tabs.old import Parser


class ParserTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Table([]), Parser().table_from_chunk([]))

    def test_blank(self):
        self.assertEqual(Table([Row([""], "\n")]), Parser().table_from_chunk([""]))

    def test_chunk(self):
        text = dedent("""
            foo\tb
            or
            f\tbar
        """).strip().splitlines()

        expected = Table([
            Row(["foo", "b"], "\n"),
            Row(["or"], "\n"),
            Row(["f", "bar"], "\n"),
        ])

        self.assertEqual(expected, Parser().table_from_chunk(text))


if __name__ == '__main__':
    unittest.main()
