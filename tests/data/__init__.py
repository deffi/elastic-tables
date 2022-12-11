from pathlib import Path
from typing import Tuple, Optional


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


def test_case_data(prefix: str, suffix: Optional[str] = None) -> Tuple[str, str]:
    input_path, expected_path = test_case(prefix, suffix)
    return input_path.read_text(), expected_path.read_text()
