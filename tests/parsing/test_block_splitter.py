import unittest

from elastic_tabs.model import Line, Block
from elastic_tabs.parsing import BlockSplitter

blank = Line("", "\n")
foo = Line("foo", "\n")
bar = Line("bar", "\n")
v_bar = Line("\vbar", "\n")
bar_v = Line("bar\v", "\n")
baz = Line("bar", "\n")


class BlockSplitterTest(unittest.TestCase):
    def test_vertical_tab_beginning(self):
        splitter = BlockSplitter()

        splitter.input([foo, v_bar, baz])
        splitter.flush()
        self.assertEqual([Block([foo]), Block([bar, baz])], splitter.blocks())

        splitter.input([foo, v_bar, baz])
        splitter.flush()
        self.assertEqual([Block([foo]), Block([bar, baz])], splitter.blocks())

    def test_vertical_tab_end(self):
        splitter = BlockSplitter()
        splitter.input([foo, bar_v, baz])
        splitter.flush()
        self.assertEqual([Block([foo, bar]), Block([baz])], splitter.blocks())

    def test_blank_line(self):
        splitter = BlockSplitter()
        splitter.input([foo, blank, baz])
        splitter.flush()
        # TODO should the blank line be in a separate block?
        self.assertEqual([Block([foo, blank]), Block([baz])], splitter.blocks(clear=False))
        self.assertEqual([Block([foo, blank]), Block([baz])], splitter.blocks())
        self.assertEqual([], splitter.blocks())

    def test_flush(self):
        splitter = BlockSplitter()
        self.assertEqual([], splitter.blocks())

        splitter.flush()
        self.assertEqual([], splitter.blocks())

        splitter.flush()
        splitter.flush()
        self.assertEqual([], splitter.blocks())


if __name__ == '__main__':
    unittest.main()
