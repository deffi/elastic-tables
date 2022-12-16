import pytest

from elastic_tables.model import Cell


def ljust(text: str, length: int) -> str: return text.ljust(length)
def rjust(text: str, length: int) -> str: return text.rjust(length)


class TestCell:
    def test_default_alignment(self):
        assert Cell("foo", None).render(3, None) == "foo"
        assert Cell("foo", None).render(4, None) == "foo "
        with pytest.raises(ValueError):
            Cell("foo", None).render(2, None)

    def test_alignment(self):
        assert Cell("foo", rjust).render(4, None) == " foo"
        assert Cell("foo", None).render(4, rjust) == " foo"
        assert Cell("foo", rjust).render(4, rjust) == " foo"

        # Cell alignment has priority over default alignment
        assert Cell("foo", rjust).render(4, ljust) == " foo"
        assert Cell("foo", ljust).render(4, rjust) == "foo "
