import pytest

from ykp.indicators import simple_moving_average, bollinger_bands, relative_strength_index


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

def test_bollinger_bands_constant():
    data = [1.0, 1.0, 1.0, 1.0, 1.0]
    lower, upper = bollinger_bands(data, window=3, num_std=1.0)
    assert lower == [None, None, 1.0, 1.0, 1.0]
    assert upper == [None, None, 1.0, 1.0, 1.0]

def test_bollinger_bands_invalid_window():
    with pytest.raises(ValueError):
        bollinger_bands([1, 2, 3], 0, 1.0)

def test_bollinger_bands_invalid_num_std():
    with pytest.raises(ValueError):
        bollinger_bands([1, 2, 3], 3, -1.0)

def test_rsi_constant_gain():
    data = [0.0, 1.0, 2.0, 3.0, 4.0]
    rsi = relative_strength_index(data, window=3)
    assert rsi[:3] == [None, None, None]
    assert all(val == 100.0 for val in rsi[3:])

def test_rsi_invalid_window():
    with pytest.raises(ValueError):
        relative_strength_index([1, 2, 3], 0)
