"""
Module for running backtests on trading strategies.
"""

from typing import List, Dict, Any, Union
try:
    import pandas as pd
    import numpy as np
    _PANDAS_AVAILABLE = True
except ImportError:
    pd = None  # type: ignore
    np = None  # type: ignore
    _PANDAS_AVAILABLE = False


class Backtester:
    """
    Engine to backtest a trading strategy on historical price data.
    """
    def __init__(self, strategy: Any, initial_cash: float = 10000.0):
        self.strategy = strategy
        self.initial_cash = initial_cash

    def run(self, prices: List[float]) -> Dict[str, Any]:
        """
        Execute the backtest given a list of price data.

        :param prices: List of price values.
        :returns: Dictionary containing equity curve and returns.
        """
        signals = self.strategy.generate_signals(prices)
        # pandas/NumPy vectorized path
        if _PANDAS_AVAILABLE and isinstance(prices, pd.Series):
            sig = pd.Series(signals, index=prices.index)
            buy = (sig == 1).astype(int)
            sell = (sig == -1).astype(int)
            position = (buy - sell).cumsum().clip(lower=0)
            cash = self.initial_cash - (buy * prices - sell * prices).cumsum()
            equity = cash + position * prices
            returns = equity.pct_change().fillna(0)
            return {"equity_curve": equity, "returns": returns}
        # fallback to Python implementation
        cash = self.initial_cash
        position = 0
        equity_curve: List[float] = []
        for price, signal in zip(prices, signals):
            if signal == 1 and cash >= price:
                position += 1
                cash -= price
            elif signal == -1 and position > 0:
                position -= 1
                cash += price
            equity_curve.append(cash + position * price)
        returns: List[float] = []
        for i in range(1, len(equity_curve)):
            prev = equity_curve[i - 1]
            curr = equity_curve[i]
            returns.append((curr - prev) / prev if prev else 0.0)
        return {"equity_curve": equity_curve, "returns": returns}
