from pathlib import Path
from typing import Iterator, Tuple


def test_cases() -> Iterator[Tuple[str, Path, str]]:
    """Yields prefix, input_path, expected_text"""

    for input_path in Path(__file__).parent.glob("*_in.txt"):
        prefix = input_path.stem.removesuffix("_in")
        expected_path = input_path.with_stem(f"{prefix}_expected")

        yield prefix, input_path, expected_path.read_text()
