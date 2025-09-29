"""
Module for calculating technical indicators.
"""

from typing import List, Optional

def simple_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    Compute the simple moving average (SMA) over a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for the moving average (must be > 0).
    :returns: List of SMA values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    sma: List[Optional[float]] = []
    for i in range(len(data)):
        if i + 1 < window:
            sma.append(None)
        else:
            window_sum = sum(data[i + 1 - window : i + 1])
            sma.append(window_sum / window)
    return sma
