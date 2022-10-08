from pathlib import Path
import sys
from typing import Optional

import typer

from elastic_tabs import StreamFilter


def do_filter(file):
    f = StreamFilter(sys.stdout)

    # Don't read the whole thing at once so we can use it in a shell
    # pipeline
    # TODO does this recognize the same line breaks as str.splitlines?
    # TODO how does this treat trailing newlines?
    for line in file:
        print(line.strip(), file=f)

    f.flush()


def main(file_name: Optional[Path] = typer.Argument(None)):
    if file_name is None:
        do_filter(sys.stdin)
    else:
        with open(file_name, "r") as file:
            do_filter(file)


if __name__ == "__main__":
    typer.run(main)
