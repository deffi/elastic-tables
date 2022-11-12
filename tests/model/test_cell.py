import unittest

from elastic_tables.model import Cell


def ljust(text: str, length: int) -> str: return text.ljust(length)
def rjust(text: str, length: int) -> str: return text.rjust(length)


class CellTest(unittest.TestCase):
    def test_default_alignment(self):
        self.assertEqual("foo", Cell("foo", None).render(3, None))
        self.assertEqual("foo ", Cell("foo", None).render(4, None))
        with self.assertRaises(ValueError):
            Cell("foo", None).render(2, None)

    def test_alignment(self):
        self.assertEqual(" foo", Cell("foo", rjust).render(4, None))
        self.assertEqual(" foo", Cell("foo", None).render(4, rjust))
        self.assertEqual(" foo", Cell("foo", rjust).render(4, rjust))

        # Cell alignment has priority over default alignment
        self.assertEqual(" foo", Cell("foo", rjust).render(4, ljust))
        self.assertEqual("foo ", Cell("foo", ljust).render(4, rjust))


if __name__ == '__main__':
    unittest.main()
