import re

from elastic_tables.model import Column, Cell


class TestColumn:
    def test_width(self):
        assert Column([]).width() == 0
        assert Column([Cell("")]).width() == 0
        assert Column([Cell(""), Cell(""), Cell("")]).width() == 0
        assert Column([Cell("a")]).width() == 1
        assert Column([Cell("a"), Cell("aaa"), Cell(""), Cell("aa")]).width() == 3

    def test_match(self):
        numeric = re.compile(r'\d+')

        assert not Column([Cell("a"), Cell("aa")]).matches(numeric)
        assert     Column([Cell("1"), Cell("11")]).matches(numeric)
        assert not Column([Cell("1"), Cell("a")]).matches(numeric)
