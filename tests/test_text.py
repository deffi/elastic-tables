import unittest

from elastic_tabs.text import splitlines


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


if __name__ == '__main__':
    unittest.main()
