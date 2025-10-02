import pytest

from quanttools.strategy import OptionBuyAndHoldStrategy, OptionStraddleStrategy


def test_option_buy_and_hold_basic():
    strat = OptionBuyAndHoldStrategy()
    prices = [10.0, 20.0, 30.0]
    signals = strat.generate_signals(prices)
    assert signals == [1, 0, 0]


def test_option_buy_and_hold_empty():
    strat = OptionBuyAndHoldStrategy()
    assert strat.generate_signals([]) == []


def test_option_straddle_basic():
    strat = OptionStraddleStrategy(threshold=0.2)
    iv = [0.1, 0.3, 0.2]
    signals = strat.generate_signals(iv)
    assert signals == [0, 1, 0]


def test_option_straddle_invalid_threshold():
    with pytest.raises(ValueError):
        OptionStraddleStrategy(threshold=-0.1)
