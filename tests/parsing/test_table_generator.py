import unittest

from elastic_tables.model import Table, Row, Block, Line
from elastic_tables.parsing import TableGenerator


class TableGeneratorTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(Table([]), TableGenerator().table_from_block(Block([])))

    def test_blank(self):
        self.assertEqual(Table([Row([""], "")]), TableGenerator().table_from_block(Block([
            Line("", ""),
        ])))

    def test_block(self):
        block = Block([
            Line("foo\tb", "\n"),
            Line("or", "\n"),
            Line("f\tbar", "\n"),
        ])

        expected = Table([
            Row(["foo", "b"], "\n"),
            Row(["or"], "\n"),
            Row(["f", "bar"], "\n"),
        ])

        self.assertEqual(expected, TableGenerator().table_from_block(block))


if __name__ == '__main__':
    unittest.main()
