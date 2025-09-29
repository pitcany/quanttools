"""
Module for defining trading strategy interfaces and implementations.
"""

from typing import List


class Strategy:
    """
    Base class for trading strategies.
    """
    def generate_signals(self, prices: List[float]) -> List[int]:
        """
        Generate trading signals based on price data.

        :param prices: List of price values.
        :returns: List of signals (1=buy, -1=sell, 0=hold).
        """
        raise NotImplementedError("Strategy.generate_signals must be implemented by subclass.")


class MovingAverageCrossStrategy(Strategy):
    """
    Simple moving average crossover strategy.
    Buys when short-term MA crosses above long-term MA and sells on reverse.
    """
    def __init__(self, short_window: int, long_window: int):
        if short_window >= long_window:
            raise ValueError("short_window must be less than long_window")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import simple_moving_average

        short_ma = simple_moving_average(prices, self.short_window)
        long_ma = simple_moving_average(prices, self.long_window)
        signals: List[int] = []
        for s, l in zip(short_ma, long_ma):
            if s is None or l is None:
                signals.append(0)
            elif s > l:
                signals.append(1)
            elif s < l:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class RSIStrategy(Strategy):
    """
    Relative Strength Index (RSI) strategy.
    Buys when RSI falls below buy_threshold and sells when RSI rises above sell_threshold.
    """
    def __init__(self, window: int, buy_threshold: float = 30.0, sell_threshold: float = 70.0):
        if window < 1:
            raise ValueError("Window size must be positive")
        if buy_threshold > sell_threshold:
            raise ValueError("buy_threshold must be <= sell_threshold")
        self.window = window
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import relative_strength_index

        rsi_values = relative_strength_index(prices, self.window)
        signals: List[int] = []
        for val in rsi_values:
            if val is None:
                signals.append(0)
            elif val < self.buy_threshold:
                signals.append(1)
            elif val > self.sell_threshold:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class BollingerBandsStrategy(Strategy):
    """
    Bollinger Bands strategy.
    Buys when price falls below lower band and sells when price rises above upper band.
    """
    def __init__(self, window: int, num_std: float):
        if window < 1:
            raise ValueError("Window size must be positive")
        if num_std < 0:
            raise ValueError("num_std must be non-negative")
        self.window = window
        self.num_std = num_std

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import bollinger_bands

        lower_band, upper_band = bollinger_bands(prices, self.window, self.num_std)
        signals: List[int] = []
        for price, l, u in zip(prices, lower_band, upper_band):
            if l is None or u is None:
                signals.append(0)
            elif price < l:
                signals.append(1)
            elif price > u:
                signals.append(-1)
            else:
                signals.append(0)
        return signals
