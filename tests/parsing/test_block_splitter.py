import unittest

from typing import Iterable, Sequence

from elastic_tables.model import Line, Block
from elastic_tables.parsing import BlockSplitter


def lines(*strings: str) -> Sequence[Line]:
    return [Line(string, "\n") for string in strings]


def blocks(*groups: Iterable[str]) -> Sequence[Block]:
    return [Block(lines(*group)) for group in groups]


class BlockSplitterTest(unittest.TestCase):
    ###########
    # General #
    ###########

    def setUp(self) -> None:
        self.splitter = BlockSplitter()

    def assertSplitBlock(self, expected: Iterable[Iterable[str]], line_contents: Iterable[str], iterations: int = 3):
        for i in range(iterations):
            self.splitter.input(lines(*line_contents))
            self.splitter.flush()
            self.assertEqual(blocks(*expected), self.splitter.blocks(clear=False))
            self.assertEqual(blocks(*expected), self.splitter.blocks())
            self.assertEqual([], self.splitter.blocks())

    ################
    # Single block #
    ################

    def test_empty_block(self):
        self.assertSplitBlock([
        ], [
        ])

    def test_single_block(self):
        self.assertSplitBlock([
            ["foo", "bar", "baz"],
        ], [
            "foo",
            "bar",
            "baz",
        ])

    ##############
    # Blank line #
    ##############

    def test_split_on_blank_line(self):
        # TODO should the blank line be in a separate block?
        self.assertSplitBlock([
            ["foo", ""],
            ["baz"],
        ], [
            "foo",
            "",
            "baz",
        ])

    ################
    # Vertical tab #
    ################

    def test_split_on_vertical_tab_beginning(self):
        self.assertSplitBlock([
            ["foo"],
            ["bar", "baz"]
        ], [
            "foo",
            "\vbar",
            "baz",
        ])

    def test_split_on_vertical_tab_end(self):
        self.assertSplitBlock([
            ["foo", "bar"],
            ["baz"]
        ], [
            "foo",
            "bar\v",
            "baz",
        ])

    ##################
    # Extra flushing #
    ##################

    def test_flush(self):
        self.assertEqual([], self.splitter.blocks())

        self.splitter.flush()
        self.assertEqual([], self.splitter.blocks())

        self.splitter.flush()
        self.splitter.flush()
        self.assertEqual([], self.splitter.blocks())


if __name__ == '__main__':
    unittest.main()
