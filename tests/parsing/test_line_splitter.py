from elastic_tables.model import Line
from elastic_tables.parsing import LineSplitter


foo = Line("foo", "\n")
bar_baz = Line("barbaz", "\n")
qux = Line("qux", "")


class TestLineSplitter:
    def test_simple(self):
        splitter = LineSplitter(None)

        splitter.input("foo\n")
        assert splitter.lines(clear=False) == [foo]
        assert splitter.lines() == [foo]
        assert splitter.lines() == []

        splitter.input("foo\n")
        assert splitter.lines(clear=False) == [foo]
        assert splitter.lines() == [foo]
        assert splitter.lines() == []

    def test_multiple(self):
        splitter = LineSplitter(None)
        assert splitter.lines(clear=False) == []

        splitter.input("foo\n")
        assert splitter.lines(clear=False) == [foo]

        splitter.input("bar")
        assert splitter.lines(clear=False) == [foo]

        splitter.input("baz\n")
        assert splitter.lines(clear=False) == [foo, bar_baz]

        splitter.input("qux")
        assert splitter.lines(clear=False) == [foo, bar_baz]

        splitter.flush()
        assert splitter.lines(clear=False) == [foo, bar_baz, qux]
        assert splitter.lines() == [foo, bar_baz, qux]
        assert splitter.lines() == []

    def test_flush(self):
        splitter = LineSplitter()
        assert splitter.lines() == []

        splitter.flush()
        assert splitter.lines() == []

        splitter.flush()
        splitter.flush()
        assert splitter.lines() == []
