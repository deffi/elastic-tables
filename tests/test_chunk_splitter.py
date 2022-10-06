import unittest

from elastic_tabs import ChunkSplitter


class ChunkSplitterTest(unittest.TestCase):
    def test_vertical_tab_beginning(self):
        splitter = ChunkSplitter()
        splitter.add_lines(["foo", "\vbar", "baz"])
        splitter.flush()
        self.assertEqual([["foo"], ["bar", "baz"]], list(splitter))

    def test_vertical_tab_end(self):
        splitter = ChunkSplitter()
        splitter.add_lines(["foo", "bar\v", "baz"])
        splitter.flush()
        self.assertEqual([["foo", "bar"], ["baz"]], list(splitter))

    def test_blank_line(self):
        splitter = ChunkSplitter()
        splitter.add_lines(["foo", "", "bar"])
        splitter.flush()
        self.assertEqual([["foo", ""], ["bar"]], list(splitter))

    def test_chunks_from_lines(self):
        splitter = ChunkSplitter()
        self.assertEqual([["foo", ""], ["bar"]], list(splitter.chunks_from_lines(["foo", "", "bar"])))


if __name__ == '__main__':
    unittest.main()
