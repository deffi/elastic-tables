from pathlib import Path
import sys
from typing import Optional, TextIO

import typer

from elastic_tabs.filter import StreamFilter


def do_filter(file: TextIO) -> None:
    f = StreamFilter(sys.stdout)

    # Read line by line so we can use it in a shell pipeline without blocking
    while (string := file.readline()) != "":
        f.write(string)

    f.flush()


def cli(file_name: Optional[Path] = typer.Argument(None)) -> None:
    if file_name is None:
        do_filter(sys.stdin)
    else:
        with open(file_name, "r") as file:
            do_filter(file)


def main():
    typer.run(cli)


if __name__ == "__main__":
    main()
