from pathlib import Path
from typing import Iterator, Tuple, Optional


_root = Path(__file__).parent


def test_case(prefix: str, suffix: Optional[str] = None) -> Tuple[Path, Path]:
    """Returns input_path, expected_path"""

    if suffix:
        suffix = "_" + suffix
    else:
        suffix = ""

    input_path = _root / f"{prefix}_in.txt"
    expected_path = _root / f"{prefix}_expected{suffix}.txt"

    return input_path, expected_path
