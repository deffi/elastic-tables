import unittest

from tab_les.model import Row, Line


class RowTest(unittest.TestCase):
    def test_from_line(self):
        self.assertEqual(Row(["foo", "bar"], "\n"), Row.from_line(Line("foo\tbar", "\n")))


if __name__ == '__main__':
    unittest.main()
