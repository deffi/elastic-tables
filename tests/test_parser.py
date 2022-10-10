import unittest
from textwrap import dedent

from elastic_tabs.model import Table
from elastic_tabs import Parser


class ParserTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Table([]), Parser().table_from_chunk([]))

    def test_blank(self):
        self.assertEqual(Table([[""]]), Parser().table_from_chunk([""]))

    def test_chunk(self):
        text = dedent("""
            foo\tb
            or
            f\tbar
        """).strip().splitlines()

        expected = Table([
            ["foo", "b"],
            ["or"],
            ["f", "bar"],
        ])

        self.assertEqual(expected, Parser().table_from_chunk(text))


if __name__ == '__main__':
    unittest.main()
