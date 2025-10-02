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


class ExponentialMovingAverageCrossStrategy(Strategy):
    """
    Exponential moving average crossover strategy.
    Buys when short-term EMA crosses above long-term EMA and sells on reverse.
    """
    def __init__(self, short_window: int, long_window: int):
        if short_window >= long_window:
            raise ValueError("short_window must be less than long_window")
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import exponential_moving_average

        short_ema = exponential_moving_average(prices, self.short_window)
        long_ema = exponential_moving_average(prices, self.long_window)
        signals: List[int] = []
        for s, l in zip(short_ema, long_ema):
            if s is None or l is None:
                signals.append(0)
            elif s > l:
                signals.append(1)
            elif s < l:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class MACDStrategy(Strategy):
    """
    Moving Average Convergence Divergence (MACD) strategy.
    Buys when MACD line crosses above signal line and sells on reverse.
    """
    def __init__(self, fast_window: int = 12, slow_window: int = 26, signal_window: int = 9):
        if fast_window < 1 or slow_window < 1 or signal_window < 1:
            raise ValueError("Window sizes must be positive")
        if fast_window >= slow_window:
            raise ValueError("fast_window must be less than slow_window")
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.signal_window = signal_window

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import macd

        macd_line, signal_line = macd(prices, self.fast_window, self.slow_window, self.signal_window)
        signals: List[int] = []
        for m, s in zip(macd_line, signal_line):
            if m is None or s is None:
                signals.append(0)
            elif m > s:
                signals.append(1)
            elif m < s:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class MomentumStrategy(Strategy):
    """
    Momentum strategy.
    Buys when momentum exceeds positive threshold and sells when below negative threshold.
    """
    def __init__(self, window: int, threshold: float = 0.0):
        if window < 1:
            raise ValueError("Window size must be positive")
        self.window = window
        self.threshold = threshold

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import momentum

        mom_vals = momentum(prices, self.window)
        signals: List[int] = []
        for m in mom_vals:
            if m is None:
                signals.append(0)
            elif m > self.threshold:
                signals.append(1)
            elif m < -self.threshold:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class ROCStrategy(Strategy):
    """
    Rate of Change (ROC) strategy.
    Buys when ROC exceeds positive threshold and sells when below negative threshold.
    """
    def __init__(self, window: int, threshold: float = 0.0):
        if window < 1:
            raise ValueError("Window size must be positive")
        self.window = window
        self.threshold = threshold

    def generate_signals(self, prices: List[float]) -> List[int]:
        from .indicators import rate_of_change

        roc_vals = rate_of_change(prices, self.window)
        signals: List[int] = []
        for r in roc_vals:
            if r is None:
                signals.append(0)
            elif r > self.threshold:
                signals.append(1)
            elif r < -self.threshold:
                signals.append(-1)
            else:
                signals.append(0)
        return signals


class OptionBuyAndHoldStrategy(Strategy):
    """
    Simple strategy to buy an option at the first opportunity and hold until expiration.
    """
    def generate_signals(self, prices: List[float]) -> List[int]:
        # Buy signal at time 0, hold (0) thereafter
        if not prices:
            return []
        return [1] + [0] * (len(prices) - 1)


class OptionStraddleStrategy(Strategy):
    """
    Strategy to buy a straddle when implied volatility exceeds a given threshold.
    """
    def __init__(self, threshold: float):
        if threshold < 0:
            raise ValueError("threshold must be non-negative")
        self.threshold = threshold

    def generate_signals(self, implied_vol: List[float]) -> List[int]:
        signals: List[int] = []
        for iv in implied_vol:
            signals.append(1 if iv > self.threshold else 0)
        return signals
