import unittest
import re

from elastic_tables.model import Column, Cell


class ColumnTest(unittest.TestCase):
    def test_width(self):
        self.assertEqual(0, Column([]).width())
        self.assertEqual(0, Column([Cell("")]).width())
        self.assertEqual(0, Column([Cell(""), Cell(""), Cell("")]).width())
        self.assertEqual(1, Column([Cell("a")]).width())
        self.assertEqual(3, Column([Cell("a"), Cell("aaa"), Cell(""), Cell("aa")]).width())

    def test_match(self):
        numeric = re.compile(r'\d+')

        self.assertFalse(Column([Cell("a"), Cell("aa")]).matches(numeric))
        self.assertTrue (Column([Cell("1"), Cell("11")]).matches(numeric))
        self.assertFalse(Column([Cell("1"), Cell("a")]).matches(numeric))


if __name__ == '__main__':
    unittest.main()
