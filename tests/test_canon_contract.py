import math
import pytest
from ensdg.canon import CanonError, canon_bytes


def test_rejects_float():
    with pytest.raises(CanonError):
        canon_bytes({"x": 1.5})


def test_rejects_nan():
    with pytest.raises(CanonError):
        canon_bytes({"x": math.nan})


def test_stable_key_order():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert canon_bytes(a) == canon_bytes(b)
