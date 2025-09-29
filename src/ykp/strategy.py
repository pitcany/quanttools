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
