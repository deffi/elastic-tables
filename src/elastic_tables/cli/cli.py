from pathlib import Path
import sys
from typing import Optional, TextIO

import typer

from elastic_tables.filter import StreamFilter


def do_filter(file: TextIO, align_numeric: bool, align_space: bool) -> None:
    f = StreamFilter(sys.stdout)
    f.filter.align_numeric = align_numeric
    f.filter.align_space = align_space

    # Read line by line so we can use it in a shell pipeline without blocking
    while (string := file.readline()) != "":
        f.write(string)

    f.flush()


def cli(file_name: Optional[Path] = typer.Argument(None), align_numeric: bool = True, align_space: bool = True) -> None:
    sys.stdout.reconfigure(newline='')

    if file_name is None:
        sys.stdin.reconfigure(newline='')
        do_filter(sys.stdin, align_numeric, align_space)
    else:
        with open(file_name, "r", newline='') as file:
            do_filter(file, align_numeric, align_space)


def main():
    typer.run(cli)


if __name__ == "__main__":
    main()
