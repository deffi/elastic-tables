from typing import Iterable

from elastic_tabs.filter import Filter


class StreamFilter:
    def __init__(self, stream):
        self.stream = stream
        self.filter = Filter(self._write_output)

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def _write_output(self, text_lines: Iterable[str]):
        for line in text_lines:
            self.stream.write(line)

    def write(self, data):
        self.filter.add_text(data)

    def flush(self):
        self.filter.flush()
        self.stream.flush()

# sys.stdout = MyFilter(sys.stdout)
# sys.stderr = MyFilter(sys.stderr)

