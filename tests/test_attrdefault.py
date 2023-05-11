"""
Tests for the AttrDefault class.
"""
import pytest
from dotdict.default import AttrDefault


def test_method_missing():
    default_none = AttrDefault()
    default_list = AttrDefault(list, sequence_type=None)
    default_double = AttrDefault(lambda value: value * 2, pass_key=True)

    with pytest.raises(AttributeError):
        _ = default_none.foo
    with pytest.raises(KeyError):
        _ = default_none['foo']
    assert default_none == {}

    assert default_list.foo == []
    assert default_list['bar'] == []
    assert default_list == {'foo': [], 'bar': []}

    assert default_double.foo == 'foofoo'
    assert default_double['bar'] == 'barbar'
    assert default_double == {'foo': 'foofoo', 'bar': 'barbar'}
