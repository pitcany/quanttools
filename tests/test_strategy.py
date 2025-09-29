import pytest

from ykp.strategy import MovingAverageCrossStrategy, RSIStrategy, BollingerBandsStrategy


def test_mac_strategy_valid():
    strat = MovingAverageCrossStrategy(2, 4)
    prices = [1, 2, 3, 4, 5, 6]
    signals = strat.generate_signals(prices)
    assert isinstance(signals, list)
    assert len(signals) == len(prices)


def test_mac_strategy_invalid():
    with pytest.raises(ValueError):
        MovingAverageCrossStrategy(5, 3)

def test_rsi_strategy_basic():
    strat = RSIStrategy(window=3, buy_threshold=30, sell_threshold=70)
    prices = [0, 1, 2, 3, 4, 5]
    signals = strat.generate_signals(prices)
    assert len(signals) == len(prices)
    assert signals[:3] == [0, 0, 0]
    assert signals[3:] == [-1, -1, -1]

def test_rsi_strategy_invalid_params():
    with pytest.raises(ValueError):
        RSIStrategy(0, 30, 70)
    with pytest.raises(ValueError):
        RSIStrategy(3, 80, 20)

def test_bollinger_bands_strategy_basic():
    strat = BollingerBandsStrategy(window=3, num_std=1)
    prices = [1, 1, 1, 1, 1]
    signals = strat.generate_signals(prices)
    assert signals == [0, 0, 0, 0, 0]
    prices2 = [2, 2, 2, 2, 0]
    signals2 = strat.generate_signals(prices2)
    assert signals2[-1] == 1

def test_bollinger_bands_strategy_invalid_params():
    with pytest.raises(ValueError):
        BollingerBandsStrategy(0, 1)
    with pytest.raises(ValueError):
        BollingerBandsStrategy(3, -1)
