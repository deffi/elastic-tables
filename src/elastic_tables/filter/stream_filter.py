from io import TextIOBase
from typing import Any, IO

from elastic_tables.filter import Filter


class StreamFilter(TextIOBase):
    def __init__(self, stream: IO):
        self.stream = stream
        self.filter = Filter(self._write_output)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.stream, name)

    def _write_output(self, text: str) -> None:
        self.stream.write(text)

    def write(self, data: str) -> int:
        self.filter.input(data)
        return len(data)

    def flush(self) -> None:
        self.filter.flush()
        self.stream.flush()

    def close(self) -> None:
        self.flush()
        self.stream.close()
