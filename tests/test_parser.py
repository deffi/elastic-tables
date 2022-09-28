import unittest
from textwrap import dedent

from elastic_tabs import Parser, Table


class ParserTest(unittest.TestCase):
    def test_blank_line(self):
        text = dedent("""
            foo\tb
            f\tbar
            
            foobar\tw
            f\twaldo
        """).strip().splitlines()

        tables = [Table([
            ["foo", "b"],
            ["f", "bar"],
            [""]
        ]), Table([
            ["foobar", "w"],
            ["f", "waldo"],
        ])]

        self.assertEqual(tables, list (Parser().split_tables(text)))


if __name__ == '__main__':
    unittest.main()
