from pathlib import Path
from typing import Iterator, Tuple


_root = Path(__file__).parent


def test_case(prefix: str) -> Tuple[Path, Path]:
    """Returns input_path, expected_path"""

    input_path = _root / f"{prefix}_in.txt"
    expected_path = _root / f"{prefix}_expected.txt"

    return input_path, expected_path


def test_cases() -> Iterator[Tuple[str, Path, Path]]:
    """Yields prefix, input_path, expected_path"""

    for input_path in Path(__file__).parent.glob("*_in.txt"):
        prefix = input_path.stem.removesuffix("_in")
        expected_path = input_path.with_stem(f"{prefix}_expected")

        yield prefix, input_path, expected_path
