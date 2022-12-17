import pytest

from elastic_tables.util.dict import replace_value


class TestDict:
    def test_replace_value_noop(self):
        # Empty dict
        assert replace_value({}, "xxx") == {}

        # Single-element dict
        assert replace_value({"foo": 1}, "foo") == {"foo": 1}
        assert replace_value({"foo": 1}, "xxx") == {"foo": 1}

        # Multi-element dict
        assert replace_value({"foo": 1, "bar": 2}, "foo") == {"foo": 1, "bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "bar") == {"foo": 1, "bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "xxx") == {"foo": 1, "bar": 2}

    def test_replace_value_default(self):
        # Empty dict, add default
        assert replace_value({}, "xxx", default=9) == {"xxx": 9}

        # Single-element dict, already present or add default
        assert replace_value({"foo": 1}, "foo", default=9) == {"foo": 1}
        assert replace_value({"foo": 1}, "xxx", default=9) == {"foo": 1, "xxx": 9}

        # Multi-element dict, already present or add default
        assert replace_value({"foo": 1, "bar": 2}, "foo", default=9) == {"foo": 1, "bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "bar", default=9) == {"foo": 1, "bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "xxx", default=9) == {"foo": 1, "bar": 2, "xxx": 9}

    def test_replace_value_remove(self):
        # Empty dict, remove is a noop
        assert replace_value({}, "xxx", remove=[]) == {}
        assert replace_value({}, "xxx", remove=[9]) == {}

        # Single-element dict, remove empty list
        assert replace_value({"foo": 1}, "foo", remove=[]) == {"foo": 1}
        assert replace_value({"foo": 1}, "xxx", remove=[]) == {"foo": 1}

        # Single-element dict, remove non-existing value
        assert replace_value({"foo": 1}, "foo", remove=[9]) == {"foo": 1}
        assert replace_value({"foo": 1}, "xxx", remove=[9]) == {"foo": 1}

        # Single-element dict, remove existing value
        assert replace_value({"foo": 1}, "foo", remove=[1]) == {}
        assert replace_value({"foo": 1}, "xxx", remove=[1]) == {"foo": 1}

        # Single-element dict, remove multiple values
        assert replace_value({"foo": 1}, "foo", remove=[1, 9]) == {}
        assert replace_value({"foo": 1}, "xxx", remove=[1, 9]) == {"foo": 1}

        # Multi-elemnt dict, remove matching value
        assert replace_value({"foo": 1, "bar": 2}, "foo", remove=[1]) == {"bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "bar", remove=[2]) == {"foo": 1}
        assert replace_value({"foo": 1, "bar": 2}, "xxx", remove=[2]) == {"foo": 1, "bar": 2}

        # Multi-elemnt dict, remove matching multiple values
        assert replace_value({"foo": 1, "bar": 2}, "foo", remove=[1, 2]) == {"bar": 2}
        assert replace_value({"foo": 1, "bar": 2}, "bar", remove=[1, 2]) == {"foo": 1}
        assert replace_value({"foo": 1, "bar": 2}, "xxx", remove=[1, 2]) == {"foo": 1, "bar": 2}

    def test_replace_value_default_and_remove(self):
        # Non-matching value is not removed
        assert replace_value({"foo": 1}, "foo", default=2, remove=[2]) == {"foo": 1}

        # When removing, no default is added
        assert replace_value({"foo": 1}, "foo", default=1, remove=[1]) == {}

        # Added default is not removed
        assert replace_value({}, "foo", default=1, remove=[1]) == {"foo": 1}
