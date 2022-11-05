from pathlib import Path
from typing import Iterator, Tuple


_root = Path(__file__).parent


def test_case(prefix: str) -> Tuple[Path, Path]:
    """Returns input_path, expected_path"""

    input_path = _root / f"{prefix}_in.txt"
    expected_path = _root / f"{prefix}_expected.txt"

    return input_path, expected_path
