import pytest

from typing import Iterable, Sequence

from elastic_tables.model import Line, Block
from elastic_tables.parser import BlockSplitter


def lines(*strings: str) -> Sequence[Line]:
    return [Line(string, "\n") for string in strings]


def blocks(*groups: Iterable[str]) -> Sequence[Block]:
    return [Block(lines(*group)) for group in groups]


@pytest.fixture()
def splitter():
    splitter = BlockSplitter()
    splitter.column_separator = "|"
    return splitter


class TestBlockSplitter:
    ###########
    # General #
    ###########

    def assertSplitBlock(self, splitter, expected: Iterable[Iterable[str]], line_contents: Iterable[str],
                         iterations: int = 3):
        for i in range(iterations):
            splitter.input(lines(*line_contents))
            splitter.flush()
            assert splitter.blocks(clear=False) == blocks(*expected)
            assert splitter.blocks() == blocks(*expected)
            assert splitter.blocks() == []

    ################
    # Single block #
    ################

    def test_no_lines(self, splitter):
        self.assertSplitBlock(splitter, [
        ], [
        ])

    def test_single_block(self, splitter):
        self.assertSplitBlock(splitter, [
            ["foo|1", "bar|2", "baz|3"],
        ], [
            "foo|1",
            "bar|2",
            "baz|3",
        ])

    #####################################
    # Splitting on single-column blocks #
    #####################################

    def test_single_column_lines(self, splitter):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock(splitter, [
            ["foo"],
            ["bar"],
            ["baz"],
        ], [
            "foo",
            "bar",
            "baz",
        ])

    def test_split_before_multi_column_block(self, splitter):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock(splitter, [
            ["foo"],
            ["bar|1", "baz|2"],
        ], [
            "foo",
            "bar|1",
            "baz|2",
        ])

    def test_split_after_multi_column_block(self, splitter):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock(splitter, [
            ["foo|1", "bar|2"],
            ["baz"],
        ], [
            "foo|1",
            "bar|2",
            "baz",
        ])

    def test_split_single_and_multi_column_blocks(self, splitter):
        # Single-column lines are simply passed through (there is no need to
        # accumulate them
        self.assertSplitBlock(splitter, [
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

    def test_split_on_blank_line(self, splitter):
        self.assertSplitBlock(splitter, [
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

    def test_split_on_vertical_tab_beginning(self, splitter):
        self.assertSplitBlock(splitter, [
            ["foo|1"],
            ["bar|2", "baz|3"]
        ], [
            "foo|1",
            "\vbar|2",
            "baz|3",
        ])

    def test_split_on_vertical_tab_end(self, splitter):
        self.assertSplitBlock(splitter, [
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

    def test_flush(self, splitter):
        assert splitter.blocks() == []

        splitter.flush()
        assert splitter.blocks() == []

        splitter.flush()
        splitter.flush()
        assert splitter.blocks() == []
