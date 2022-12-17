import pytest

from elastic_tables.util.sequence import replace_value


class TestSequence:
    def test_replace_value_noop(self):
        # Empty list
        assert replace_value([], "xxx") == []

        # Isolated argument
        assert replace_value(["foo", 1], "foo") == ["foo", 1]
        assert replace_value(["foo", 1], "xxx") == ["foo", 1]

        # Other values
        assert replace_value(["a", "foo", 1, "b"], "foo") == ["a", "foo", 1, "b"]
        assert replace_value(["b", "foo", 1, "b"], "xxx") == ["b", "foo", 1, "b"]

    def test_replace_value_default(self):
        # Empty list, add default
        assert replace_value([], "xxx", default=9) == ["xxx", 9]

        # Isolated argument, already present or add default
        assert replace_value(["foo", 1], "foo", default=9) == ["foo", 1]
        assert replace_value(["foo", 1], "xxx", default=9) == ["foo", 1, "xxx", 9]

        # Other values, already present or add default
        assert replace_value(["a", "foo", 1, "b"], "foo", default=9) == ["a", "foo", 1, "b"]
        assert replace_value(["a", "foo", 1, "b"], "xxx", default=9) == ["a", "foo", 1, "b", "xxx", 9]

    def test_replace_value_remove(self):
        # Empty list, remove is a noop
        assert replace_value([], "xxx", remove=[]) == []
        assert replace_value([], "xxx", remove=[9]) == []

        # Isolated argument, remove empty list
        assert replace_value(["foo", 1], "foo", remove=[]) == ["foo", 1]
        assert replace_value(["foo", 1], "xxx", remove=[]) == ["foo", 1]

        # Isolated argument, remove non-existing value
        assert replace_value(["foo", 1], "foo", remove=[9]) == ["foo", 1]
        assert replace_value(["foo", 1], "xxx", remove=[9]) == ["foo", 1]

        # Isolated argument, remove existing value
        assert replace_value(["foo", 1], "foo", remove=[1]) == []
        assert replace_value(["foo", 1], "xxx", remove=[1]) == ["foo", 1]

        # Isolated argument, remove multiple values
        assert replace_value(["foo", 1], "foo", remove=[1, 9]) == []
        assert replace_value(["foo", 1], "xxx", remove=[1, 9]) == ["foo", 1]

        # Other values, remove matching value
        assert replace_value(["a", "foo", 1, "b"], "foo", remove=[1]) == ["a", "b"]
        assert replace_value(["a", "foo", 1, "b"], "xxx", remove=[2]) == ["a", "foo", 1, "b"]

        # Other values, remove matching multiple values
        assert replace_value(["a", "foo", 1, "b"], "foo", remove=[1, 2]) == ["a", "b"]
        assert replace_value(["a", "foo", 1, "b"], "xxx", remove=[1, 2]) == ["a", "foo", 1, "b"]

    def test_replace_value_default_and_remove(self):
        # Non-matching value is not removed
        assert replace_value(["foo", 1], "foo", default=9, remove=[9]) == ["foo", 1]

        # When removing, no default is added
        assert replace_value(["foo", 1], "foo", default=1, remove=[1]) == []

        # Added default is not removed
        assert replace_value([], "foo", default=1, remove=[1]) == ["foo", 1]

    def test_replace_value_invalid_at_end(self):
        # Key at the end of single-element list
        with pytest.raises(ValueError):
            replace_value(["foo"], "foo")

        # Key at the end of multi-element list
        with pytest.raises(ValueError):
            replace_value(["a", "foo"], "foo")

    def test_replace_value_invalid_repeated(self):
        # Key appears mltiple times
        with pytest.raises(ValueError):
            replace_value(["foo", 1, "foo", 2], "foo")
