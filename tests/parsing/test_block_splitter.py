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
        self.splitter.column_separator = "|"

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

    def test_no_lines(self):
        self.assertSplitBlock([
        ], [
        ])

    def test_single_block(self):
        self.assertSplitBlock([
            ["foo|1", "bar|2", "baz|3"],
        ], [
            "foo|1",
            "bar|2",
            "baz|3",
        ])

    #####################################
    # Splitting on single-column blocks #
    #####################################

    def test_single_column_lines(self):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock([
            ["foo"],
            ["bar"],
            ["baz"],
        ], [
            "foo",
            "bar",
            "baz",
        ])

    def test_split_before_multi_column_block(self):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock([
            ["foo"],
            ["bar|1", "baz|2"],
        ], [
            "foo",
            "bar|1",
            "baz|2",
        ])

    def test_split_after_multi_column_block(self):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock([
            ["foo|1", "bar|2"],
            ["baz"],
        ], [
            "foo|1",
            "bar|2",
            "baz",
        ])

    def test_split_single_and_multi_column_blocks(self):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock([
            ["a|1", "b|2"],
            ["foo"],
            ["bar"],
            ["c|3", "d|4"],
            ["baz"],
            ["qux"],
        ], [
            "a|1",
            "b|2",
            "foo",
            "bar",
            "c|3",
            "d|4",
            "baz",
            "qux",
        ])

    ##############
    # Blank line #
    ##############

    def test_split_on_blank_line(self):
        self.assertSplitBlock([
            ["foo|1"],
            [""],
            ["baz|2"],
        ], [
            "foo|1",
            "",
            "baz|2",
        ])

    ################
    # Vertical tab #
    ################

    def test_split_on_vertical_tab_beginning(self):
        self.assertSplitBlock([
            ["foo|1"],
            ["bar|2", "baz|3"]
        ], [
            "foo|1",
            "\vbar|2",
            "baz|3",
        ])

    def test_split_on_vertical_tab_end(self):
        self.assertSplitBlock([
            ["foo|1", "bar|2"],
            ["baz|3"]
        ], [
            "foo|1",
            "bar|2\v",
            "baz|3",
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
