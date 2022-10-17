import unittest

from elastic_tabs.util.iterable import grouper


class IterableTest(unittest.TestCase):
    def test_grouper(self):
        # Empty
        self.assertEqual([], list(grouper(3, [])))

        # Single element
        self.assertEqual([(1, None, None)], list(grouper(3, [1])))

        # Exact multiple
        self.assertEqual([(1, 2, 3), (4, 5, 6)], list(grouper(3, [1, 2, 3, 4, 5, 6])))

        # Padded
        self.assertEqual([(1, 2, 3), (4, 5, None)], list(grouper(3, [1, 2, 3, 4, 5])))

        # n=1
        self.assertEqual([(1,), (2,), (3,)], list(grouper(1, [1, 2, 3])))

        # n=0
        with self.assertRaises(ValueError):
            grouper(0, [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
