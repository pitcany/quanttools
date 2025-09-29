"""
Module for calculating technical indicators.
"""

from typing import List, Optional, Tuple
import statistics

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

def bollinger_bands(data: List[float], window: int, num_std: float) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    """
    Compute Bollinger Bands (lower and upper) over a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for computing the moving average and std deviation (must be > 0).
    :param num_std: Number of standard deviations for the bands (must be >= 0).
    :returns: Tuple of two lists (lower_band, upper_band) with None for entries with insufficient data.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    if num_std < 0:
        raise ValueError("num_std must be non-negative")
    lower: List[Optional[float]] = []
    upper: List[Optional[float]] = []
    for i in range(len(data)):
        if i + 1 < window:
            lower.append(None)
            upper.append(None)
        else:
            window_data = data[i + 1 - window : i + 1]
            mean = sum(window_data) / window
            std = statistics.pstdev(window_data)
            lower.append(mean - num_std * std)
            upper.append(mean + num_std * std)
    return lower, upper

def relative_strength_index(data: List[float], window: int) -> List[Optional[float]]:
    """
    Compute the Relative Strength Index (RSI) for a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for RSI calculation (must be > 0).
    :returns: List of RSI values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    rsi_values: List[Optional[float]] = []
    for i in range(len(data)):
        if i < window:
            rsi_values.append(None)
        else:
            window_data = data[i + 1 - window : i + 1]
            diffs = [window_data[j] - window_data[j - 1] for j in range(1, len(window_data))]
            avg_gain = sum(d for d in diffs if d > 0) / len(diffs) if diffs else 0.0
            avg_loss = sum(-d for d in diffs if d < 0) / len(diffs) if diffs else 0.0
            if avg_loss == 0.0:
                rsi_val = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi_val = 100.0 - (100.0 / (1.0 + rs))
            rsi_values.append(rsi_val)
    return rsi_values
