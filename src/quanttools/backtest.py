"""
Module for running backtests on trading strategies.
"""

from typing import List, Dict, Any


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
