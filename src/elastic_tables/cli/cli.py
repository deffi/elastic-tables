from pathlib import Path
import sys
from typing import Optional, TextIO

import typer

from elastic_tables.filter import StreamFilter


def do_filter(file: TextIO, column_separator: str, align_numeric: bool, align_space: bool) -> None:
    f = StreamFilter(sys.stdout)
    f.filter.column_separator = column_separator
    f.filter.align_numeric = align_numeric
    f.filter.align_space = align_space

    # Read line by line so we can use it in a shell pipeline without blocking
    while (string := file.readline()) != "":
        f.write(string)

    f.flush()


def cli(file_name: Optional[Path] = typer.Argument(None),
        column_separator: str = "\t",
        align_numeric: bool = False,
        align_space: bool = False) -> None:
    sys.stdout.reconfigure(newline='')

    if file_name is None:
        sys.stdin.reconfigure(newline='')
        do_filter(sys.stdin, column_separator, align_numeric, align_space)
    else:
        with open(file_name, "r", newline='') as file:
            do_filter(file, column_separator, align_numeric, align_space)


def main():
    typer.run(cli)


if __name__ == "__main__":
    main()
