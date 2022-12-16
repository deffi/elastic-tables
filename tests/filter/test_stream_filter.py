from io import StringIO

from elastic_tables.filter import StreamFilter


class TestStreamFilter:
    def test_write(self):
        stream = StringIO()
        stream_filter = StreamFilter(stream)

        stream_filter.write("foo\tf\n")
        stream_filter.write("b\tbar\n")
        stream_filter.flush()

        assert stream.getvalue() == "foof\nb  bar\n"

    def test_print(self):
        stream = StringIO()
        stream_filter = StreamFilter(stream)

        print("foo\tf", file=stream_filter)
        print("b\tbar", file=stream_filter)
        stream_filter.flush()

        assert stream.getvalue() == "foof\nb  bar\n"
