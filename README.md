# ykp

ykp is an algorithmic trading assistant package providing tools for data loading, indicator calculation,
strategy development, backtesting, execution handling, and performance metrics.

## Installation

Install required dependencies (including core data and ML groups):

```bash
poetry install --with data,ml
```

## Quickstart

```python
from ykp import (
    simple_moving_average,
    bollinger_bands,
    relative_strength_index,
    MovingAverageCrossStrategy,
    Backtester,
    calc_max_drawdown,
)
from ykp.strategy import RSIStrategy, BollingerBandsStrategy

# Sample price series
prices = [1, 2, 3, 4, 5, 6]

# Simple Moving Average
sma = simple_moving_average(prices, window=3)

# Bollinger Bands (lower and upper)
lower_band, upper_band = bollinger_bands(prices, window=3, num_std=2.0)

# Relative Strength Index (RSI)
rsi_values = relative_strength_index(prices, window=3)

# Strategies: Moving Average Crossover, RSI, and Bollinger Bands
mac = MovingAverageCrossStrategy(short_window=2, long_window=4)
rsi_strat = RSIStrategy(window=3, buy_threshold=30, sell_threshold=70)
bb_strat = BollingerBandsStrategy(window=3, num_std=2.0)

signals_mac = mac.generate_signals(prices)
signals_rsi = rsi_strat.generate_signals(prices)
signals_bb = bb_strat.generate_signals(prices)

# Backtesting example
backtester = Backtester(mac, initial_cash=10000)
result = backtester.run(prices)
print("Equity curve:", result["equity_curve"])
print("Max Drawdown:", calc_max_drawdown(result["equity_curve"]))
```

---

## Dependency Management

To remove a dependency from your project (and uninstall it from your venv), use:

```bash
poetry remove <package-name>
```

If the package is in a specific group, specify the group via:

```bash
poetry remove <package-name> --group <group-name>
# or equivalently for dev dependencies:
poetry remove <package-name> --dev
```

# Locking and installing specific groups

To generate or install dependencies for a single optional group (e.g. `optimization`) without pulling in conflicting packages like TensorFlow, Poetry 2.4+ supports the `--only` flag:

```bash
poetry lock --only optimization
poetry install --only optimization
```

If you are on Poetry 2.2.x and cannot yet upgrade, consider using the `poetry_only_data_ml.txt` guide for workarounds or upgrading Poetry:

```bash
pipx upgrade poetry
```

# Optional Autogluon support

This project provides an optional `autogluon` dependency group to avoid dependency conflicts.
You can enable this group when locking or installing dependencies:

```bash
poetry lock --with autogluon
poetry install --with autogluon
```

For Poetry 2.4+ you can also restrict to only the `autogluon` group:

```bash
poetry lock --only autogluon
poetry install --only autogluon
```

To add Autogluon to your project, run:

```bash
poetry add autogluon-core --group autogluon
# or for full tabular support:
poetry add 'autogluon.tabular[all]' --group autogluon
```
