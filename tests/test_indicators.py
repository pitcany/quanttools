import pytest

from ykp.indicators import (
    simple_moving_average,
    bollinger_bands,
    relative_strength_index,
    exponential_moving_average,
    momentum,
    rate_of_change,
    macd,
)


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

def test_ema_basic():
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    ema = exponential_moving_average(data, window=3)
    # SMA of first 3 = 2.0, then EMA: (4-2)*0.5+2=3.0, (5-3)*0.5+3=4.0
    assert ema == [None, None, 2.0, 3.0, 4.0]

def test_ema_invalid_window():
    with pytest.raises(ValueError):
        exponential_moving_average([1, 2, 3], 0)

def test_momentum_basic():
    data = [1, 2, 3, 5]
    mom = momentum(data, window=2)
    assert mom == [None, None, 2, 3]

def test_momentum_invalid_window():
    with pytest.raises(ValueError):
        momentum([1, 2, 3], 0)

def test_roc_basic():
    data = [1.0, 2.0, 3.0, 5.0]
    roc = rate_of_change(data, window=2)
    # (3-1)/1*100 = 200, (5-2)/2*100 = 150
    assert roc == [None, None, 200.0, 150.0]

def test_roc_div_zero():
    data = [0.0, 0.0, 1.0]
    roc = rate_of_change(data, window=1)
    # first valid index 1: data[1-1]=data[0]=0.0 -> None; index 2: data[2-1]=data[1]=0.0 -> None
    assert roc == [None, None, None]

def test_macd_basic_constant():
    data = [1.0] * 35
    macd_line, signal_line = macd(data)
    # After slow_window periods, MACD line should be zero and signal line zero
    assert macd_line[-1] == 0.0
    assert signal_line[-1] == 0.0

def test_macd_invalid_params():
    with pytest.raises(ValueError):
        macd([1, 2, 3], 5, 3, 9)
    with pytest.raises(ValueError):
        macd([1, 2, 3], 12, 26, 0)
