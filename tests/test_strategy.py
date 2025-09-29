import pytest

from ykp.strategy import MovingAverageCrossStrategy


def test_mac_strategy_valid():
    strat = MovingAverageCrossStrategy(2, 4)
    prices = [1, 2, 3, 4, 5, 6]
    signals = strat.generate_signals(prices)
    assert isinstance(signals, list)
    assert len(signals) == len(prices)


def test_mac_strategy_invalid():
    with pytest.raises(ValueError):
        MovingAverageCrossStrategy(5, 3)
