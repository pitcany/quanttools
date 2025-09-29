import pytest

from ykp.indicators import simple_moving_average


def test_sma_basic():
    data = [1, 2, 3, 4, 5]
    sma = simple_moving_average(data, window=3)
    assert sma == [None, None, 2.0, 3.0, 4.0]


def test_sma_window1():
    data = [10, 20]
    sma = simple_moving_average(data, window=1)
    assert sma == [10.0, 20.0]


def test_sma_invalid_window():
    with pytest.raises(ValueError):
        simple_moving_average([1, 2, 3], 0)
