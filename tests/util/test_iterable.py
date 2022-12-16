import pytest

from elastic_tables.util.iterable import grouper


class TestIterable:
    def test_grouper(self):
        # Empty
        assert list(grouper(3, [])) == []

        # Single element
        assert [(1, None, None)] == list(grouper(3, [1]))

        # Exact multiple
        assert [(1, 2, 3), (4, 5, 6)] == list(grouper(3, [1, 2, 3, 4, 5, 6]))

        # Padded
        assert [(1, 2, 3), (4, 5, None)] == list(grouper(3, [1, 2, 3, 4, 5]))

        # n=1
        assert [(1,), (2,), (3,)] == list(grouper(1, [1, 2, 3]))

        # n=0
        with pytest.raises(ValueError):
            grouper(0, [1, 2, 3])
