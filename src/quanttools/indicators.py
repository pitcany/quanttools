"""
Module for calculating technical indicators.
"""

from typing import Sequence, Optional, Tuple, Union
import statistics
try:
    import numpy as np
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    pd = None  # type: ignore
    np = None  # type: ignore
    _PANDAS_AVAILABLE = False

def simple_moving_average(
    data: Union[Sequence[float], "pd.Series"], window: int
) -> Union[Sequence[Optional[float]], "pd.Series"]:
    """
    Compute the simple moving average (SMA) over a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for the moving average (must be > 0).
    :returns: List of SMA values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    # pandas/NumPy vectorized path
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        result = series.rolling(window=window, min_periods=window).mean()
        return result if isinstance(data, pd.Series) else result.tolist()
    # fallback to Python
    sma: list[Optional[float]] = []
    for i in range(len(data)):
        if i + 1 < window:
            sma.append(None)
        else:
            window_sum = sum(data[i + 1 - window : i + 1])
            sma.append(window_sum / window)
    return sma

def bollinger_bands(
    data: Union[Sequence[float], "pd.Series"], window: int, num_std: float
) -> Tuple[Union[Sequence[Optional[float]], "pd.Series"], Union[Sequence[Optional[float]], "pd.Series"]]:
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
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        roll = series.rolling(window=window, min_periods=window)
        mean = roll.mean()
        std = roll.std(ddof=0)
        lower = mean - num_std * std
        upper = mean + num_std * std
        if isinstance(data, pd.Series):
            return lower, upper
        return lower.tolist(), upper.tolist()
    lower: list[Optional[float]] = []
    upper: list[Optional[float]] = []
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

def relative_strength_index(
    data: Union[Sequence[float], "pd.Series"], window: int
) -> Union[Sequence[Optional[float]], "pd.Series"]:
    """
    Compute the Relative Strength Index (RSI) for a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for RSI calculation (must be > 0).
    :returns: List of RSI values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=window, min_periods=window).mean()
        avg_loss = loss.rolling(window=window, min_periods=window).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - 100 / (1 + rs)
        return rsi if isinstance(data, pd.Series) else rsi.tolist()
    rsi_values: list[Optional[float]] = []
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

def exponential_moving_average(
    data: Union[Sequence[float], "pd.Series"], window: int
) -> Union[Sequence[Optional[float]], "pd.Series"]:
    """
    Compute the exponential moving average (EMA) over a data series.

    :param data: List of float values (e.g., closing prices).
    :param window: Window size for the EMA (must be > 0).
    :returns: List of EMA values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        ema = series.ewm(span=window, adjust=False, min_periods=window).mean()
        return ema if isinstance(data, pd.Series) else ema.tolist()
    ema: list[Optional[float]] = []
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

def momentum(
    data: Union[Sequence[float], "pd.Series"], window: int
) -> Union[Sequence[Optional[float]], "pd.Series"]:
    """
    Compute the momentum indicator (difference) over a data series.

    :param data: List of float values.
    :param window: Window size for momentum (must be > 0).
    :returns: List of momentum values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        mom = series.diff(periods=window)
        return mom if isinstance(data, pd.Series) else mom.tolist()
    mom: list[Optional[float]] = []
    for i in range(len(data)):
        if i < window:
            mom.append(None)
        else:
            mom.append(data[i] - data[i - window])
    return mom

def rate_of_change(
    data: Union[Sequence[float], "pd.Series"], window: int
) -> Union[Sequence[Optional[float]], "pd.Series"]:
    """
    Compute the rate of change (ROC) percentage over a data series.

    :param data: List of float values.
    :param window: Window size for ROC (must be > 0).
    :returns: List of ROC values; entries with insufficient data are None.
    """
    if window < 1:
        raise ValueError("Window size must be positive")
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        roc = series.pct_change(periods=window) * 100
        # avoid division-by-zero entries
        roc = roc.where(series.shift(window) != 0)
        return roc if isinstance(data, pd.Series) else roc.tolist()
    roc: list[Optional[float]] = []
    for i in range(len(data)):
        if i < window or data[i - window] == 0:
            roc.append(None)
        else:
            roc.append((data[i] - data[i - window]) / data[i - window] * 100)
    return roc

def macd(
    data: Union[Sequence[float], "pd.Series"],
    fast_window: int = 12,
    slow_window: int = 26,
    signal_window: int = 9,
) -> Tuple[Union[Sequence[Optional[float]], "pd.Series"], Union[Sequence[Optional[float]], "pd.Series"]]:
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
    if _PANDAS_AVAILABLE and isinstance(data, (pd.Series, np.ndarray)):
        series = pd.Series(data)
        ema_fast = series.ewm(span=fast_window, adjust=False, min_periods=fast_window).mean()
        ema_slow = series.ewm(span=slow_window, adjust=False, min_periods=slow_window).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_window, adjust=False, min_periods=signal_window).mean()
        if isinstance(data, pd.Series):
            return macd_line, signal_line
        return macd_line.tolist(), signal_line.tolist()
    # fallback to Python implementation
    ema_fast = exponential_moving_average(data, fast_window)
    ema_slow = exponential_moving_average(data, slow_window)
    macd_line: list[Optional[float]] = []
    for f, s in zip(ema_fast, ema_slow):
        if f is None or s is None:
            macd_line.append(None)
        else:
            macd_line.append(f - s)
    # signal line is EMA of macd_line ignoring None
    signal_line: list[Optional[float]] = []
    macd_vals: list[float] = []
    for m in macd_line:
        if m is None:
            signal_line.append(None)
        else:
            macd_vals.append(m)
            if len(macd_vals) < signal_window:
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
