from elastic_tabs.filter import Filter


class StreamFilter:
    def __init__(self, stream):
        self.stream = stream
        self.filter = Filter(self._write_output)

    def __getattr__(self, name):
        return getattr(self.stream, name)

    def _write_output(self, text: str):
        self.stream.write(text)

    def write(self, data):
        self.filter.add_text(data)

    def flush(self):
        self.filter.flush()
        self.stream.flush()

    def close(self):
        self.flush()
        self.stream.close()
