"""
Module for performance and risk metric calculations.
"""

from typing import List


def calc_max_drawdown(equity_curve: List[float]) -> float:
    """
    Calculate the maximum drawdown from an equity curve.

    :param equity_curve: List of equity values over time.
    :returns: Maximum drawdown as a fraction.
    """
    if not equity_curve:
        return 0.0

    peak = equity_curve[0]
    max_dd = 0.0
    for value in equity_curve:
        if value > peak:
            peak = value
        drawdown = (peak - value) / peak if peak else 0.0
        if drawdown > max_dd:
            max_dd = drawdown
    return max_dd
