import pytest

from quanttools.strategy import (
    MovingAverageCrossStrategy,
    RSIStrategy,
    BollingerBandsStrategy,
    ExponentialMovingAverageCrossStrategy,
    MACDStrategy,
    MomentumStrategy,
    ROCStrategy,
    MeanReversionStrategy,
)


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

def test_ema_cross_strategy_basic():
    strat = ExponentialMovingAverageCrossStrategy(2, 4)
    prices = [1, 2, 3, 4, 5, 6]
    signals = strat.generate_signals(prices)
    assert isinstance(signals, list)
    assert len(signals) == len(prices)

def test_ema_cross_strategy_invalid():
    with pytest.raises(ValueError):
        ExponentialMovingAverageCrossStrategy(5, 3)

def test_macd_strategy_basic():
    strat = MACDStrategy(fast_window=2, slow_window=4, signal_window=2)
    prices = [1, 2, 3, 4, 5, 6, 7]
    signals = strat.generate_signals(prices)
    assert isinstance(signals, list)
    assert len(signals) == len(prices)

def test_macd_strategy_invalid_params():
    with pytest.raises(ValueError):
        MACDStrategy(5, 3, 2)
    with pytest.raises(ValueError):
        MACDStrategy(2, 4, 0)

def test_momentum_strategy_basic():
    strat = MomentumStrategy(window=1, threshold=0)
    prices = [1, 2, 3, 2, 1]
    # momentum: [None,1,1,-1,-1]
    signals = strat.generate_signals(prices)
    assert signals == [0, 1, 1, -1, -1]

def test_momentum_strategy_invalid():
    with pytest.raises(ValueError):
        MomentumStrategy(0, 1)

def test_roc_strategy_basic():
    strat = ROCStrategy(window=1, threshold=0)
    prices = [1, 2, 4, 2, 1]
    # roc: [None,100,100,-50,-50]
    signals = strat.generate_signals(prices)
    assert signals == [0, 1, 1, -1, -1]

def test_roc_strategy_invalid():
    with pytest.raises(ValueError):
        ROCStrategy(0, 1)

def test_mean_reversion_strategy_basic():
    strat = MeanReversionStrategy(window=2, threshold=0.0)
    prices = [1, 2, 3, 2, 1]
    # simple moving average: [None, 1.5, 2.5, 2.5, 1.5]
    signals = strat.generate_signals(prices)
    assert signals == [0, -1, -1, 1, 1]

def test_mean_reversion_strategy_threshold():
    strat = MeanReversionStrategy(window=2, threshold=1.0)
    prices = [1, 2, 3, 2, 1]
    # sma: [None, 1.5, 2.5, 2.5, 1.5]
    # thresholds: upper=mean*(1+1.0)=2*mean, lower=mean*(1-1.0)=0
    signals = strat.generate_signals(prices)
    assert signals == [0, 0, 0, 0, 0]

def test_mean_reversion_strategy_invalid_params():
    with pytest.raises(ValueError):
        MeanReversionStrategy(0, 0.1)
    with pytest.raises(ValueError):
        MeanReversionStrategy(2, -0.1)
