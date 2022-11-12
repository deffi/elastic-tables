import re
import unittest

from elastic_tables.model import Table, Row, Cell


class RenderTest(unittest.TestCase):
    def test_column_width(self):
        self.assertEqual(0, Table.column_width([]))
        self.assertEqual(0, Table.column_width([Cell("")]))
        self.assertEqual(0, Table.column_width([Cell(""), Cell(""), Cell("")]))
        self.assertEqual(1, Table.column_width([Cell("a")]))
        self.assertEqual(3, Table.column_width([Cell("a"), Cell("aaa"), Cell(""), Cell("aa")]))

    def test_column_widths(self):
        # No rows
        self.assertEqual([], Table([]).column_widths())

        # Rows with no cells each
        self.assertEqual([], Table([Row([], "\n")]).column_widths())
        self.assertEqual([], Table([Row([], "\n"), Row([], "\n")]).column_widths())

        # Single row
        self.assertEqual([1], Table([Row([Cell("a")], "\n")]).column_widths())

        # Multiple rows (different number of cells)
        self.assertEqual([3, 2], Table([Row([Cell("a"), Cell("bb")], "\n"), Row([Cell("ccc")], "\n")]).column_widths())

    def test_columns_match(self):
        table = Table([
            Row([Cell("a"),  Cell("1"),  Cell("1")], "\n"),
            Row([Cell("aa"), Cell("11"), Cell("a")], "\n"),
        ])

        numeric = re.compile(r'\d+')
        self.assertEqual([False, True, False], table.columns_match(numeric))


if __name__ == '__main__':
    unittest.main()
