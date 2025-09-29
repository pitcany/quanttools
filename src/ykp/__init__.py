"""
ykp: Algorithmic Trading Assistant Package

Provides tools for data loading, technical indicators, strategy templates,
backtesting engine, execution handling, and performance metrics.
"""

from .data import DataLoader
from .indicators import (
    simple_moving_average,
    bollinger_bands,
    relative_strength_index,
    exponential_moving_average,
    momentum,
    rate_of_change,
    macd,
)
from .strategy import (
    Strategy,
    MovingAverageCrossStrategy,
    RSIStrategy,
    BollingerBandsStrategy,
    ExponentialMovingAverageCrossStrategy,
    MACDStrategy,
    MomentumStrategy,
    ROCStrategy,
    OptionBuyAndHoldStrategy,
    OptionStraddleStrategy,
)
from .backtest import Backtester
from .execution import ExecutionHandler
from .utils import calc_max_drawdown

__all__ = [
    "DataLoader",
    "simple_moving_average",
    "bollinger_bands",
    "relative_strength_index",
    "exponential_moving_average",
    "momentum",
    "rate_of_change",
    "macd",
    "Strategy",
    "MovingAverageCrossStrategy",
    "RSIStrategy",
    "BollingerBandsStrategy",
    "ExponentialMovingAverageCrossStrategy",
    "MACDStrategy",
    "MomentumStrategy",
    "ROCStrategy",
    "OptionBuyAndHoldStrategy",
    "OptionStraddleStrategy",
    "Backtester",
    "ExecutionHandler",
    "calc_max_drawdown",
]
