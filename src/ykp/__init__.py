"""
ykp: Algorithmic Trading Assistant Package

Provides tools for data loading, technical indicators, strategy templates,
backtesting engine, execution handling, and performance metrics.
"""

from .data import DataLoader
from .indicators import simple_moving_average
from .strategy import Strategy, MovingAverageCrossStrategy
from .backtest import Backtester
from .execution import ExecutionHandler
from .utils import calc_max_drawdown

__all__ = [
    "DataLoader",
    "simple_moving_average",
    "Strategy",
    "MovingAverageCrossStrategy",
    "Backtester",
    "ExecutionHandler",
    "calc_max_drawdown",
]
