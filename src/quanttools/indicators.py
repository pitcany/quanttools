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

def exponential_moving_average(data: List[float], window: int) -> List[Optional[float]]:
    """
    Compute the exponential moving average (EMA) over a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for the EMA (must be > 0).
    :returns: List of EMA values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    ema: List[Optional[float]] = []
    multiplier = 2 / (window + 1)
    ema_prev: Optional[float] = None
    for i, price in enumerate(data):
        if i + 1 < window:
            ema.append(None)
        elif i + 1 == window:
            sma = sum(data[:window]) / window
            ema_prev = sma
            ema.append(sma)
        else:
            assert ema_prev is not None
            ema_val = (price - ema_prev) * multiplier + ema_prev
            ema.append(ema_val)
            ema_prev = ema_val
    return ema

def momentum(data: List[float], window: int) -> List[Optional[float]]:
    """
    Compute the momentum indicator (difference) over a data series.

    :param data: List of float values.
    :param window: Window size for momentum (must be > 0).
    :returns: List of momentum values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    mom: List[Optional[float]] = []
    for i in range(len(data)):
        if i < window:
            mom.append(None)
        else:
            mom.append(data[i] - data[i - window])
    return mom

def rate_of_change(data: List[float], window: int) -> List[Optional[float]]:
    """
    Compute the rate of change (ROC) percentage over a data series.

    :param data: List of float values.
    :param window: Window size for ROC (must be > 0).
    :returns: List of ROC values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    roc: List[Optional[float]] = []
    for i in range(len(data)):
        if i < window or data[i - window] == 0:
            roc.append(None)
        else:
            roc.append((data[i] - data[i - window]) / data[i - window] * 100)
    return roc

def macd(data: List[float], fast_window: int = 12, slow_window: int = 26, signal_window: int = 9) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    """
    Compute MACD line and signal line for a data series.

    :param data: List of float values.
    :param fast_window: Window size for fast EMA (must be > 0).
    :param slow_window: Window size for slow EMA (must be > fast_window).
    :param signal_window: Window size for signal line EMA (must be > 0).
    :returns: Tuple of MACD line and signal line lists; entries with insufficient data are None.
    """
    if fast_window < 1 or slow_window < 1 or signal_window < 1:
        raise ValueError("Window sizes must be positive")
    if fast_window >= slow_window:
        raise ValueError("fast_window must be less than slow_window")
    ema_fast = exponential_moving_average(data, fast_window)
    ema_slow = exponential_moving_average(data, slow_window)
    macd_line: List[Optional[float]] = []
    for f, s in zip(ema_fast, ema_slow):
        if f is None or s is None:
            macd_line.append(None)
        else:
            macd_line.append(f - s)
    # signal line is EMA of macd_line ignoring None
    # fill initial Nones for signal
    signal_line: List[Optional[float]] = []
    macd_vals: List[float] = []
    for m in macd_line:
        if m is None:
            signal_line.append(None)
        else:
            macd_vals.append(m)
            if len(macd_vals) < signal_window:
                # insufficient values for initial signal SMA
                signal_line.append(None)
            elif len(macd_vals) == signal_window:
                init_sma = sum(macd_vals) / signal_window
                signal_line.append(init_sma)
            else:
                prev = signal_line[-1]
                assert prev is not None
                mult = 2 / (signal_window + 1)
                sig = (m - prev) * mult + prev
                signal_line.append(sig)
    return macd_line, signal_line
