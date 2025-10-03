# quanttools

[![CI Tests](https://github.com/pitcany/quanttools/actions/workflows/python-ci.yml/badge.svg)](https://github.com/pitcany/quanttools/actions/workflows/python-ci.yml)

quanttools is an algorithmic trading assistant package providing tools for data loading, indicator calculation,
strategy development, backtesting, execution handling, and performance metrics.

## Installation

Install required dependencies (including core data and ML groups):

```bash
poetry install --with data,ml
```

For development (linting, testing), include the dev group:

```bash
poetry install --with data,ml,dev
```

## Quickstart

```python
from quanttools import (
    simple_moving_average,
    bollinger_bands,
    relative_strength_index,
    exponential_moving_average,
    momentum,
    rate_of_change,
    macd,
    MovingAverageCrossStrategy,
    Backtester,
    calc_max_drawdown,
)
from quanttools.strategy import (
    RSIStrategy,
    BollingerBandsStrategy,
    ExponentialMovingAverageCrossStrategy,
    MACDStrategy,
    MomentumStrategy,
    ROCStrategy,
)

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
ema_strat = ExponentialMovingAverageCrossStrategy(short_window=2, long_window=4)
macd_strat = MACDStrategy(fast_window=12, slow_window=26, signal_window=9)
mom_strat = MomentumStrategy(window=3, threshold=0.0)
roc_strat = ROCStrategy(window=3, threshold=0.0)

signals_mac = mac.generate_signals(prices)
signals_rsi = rsi_strat.generate_signals(prices)
signals_bb = bb_strat.generate_signals(prices)
signals_ema = ema_strat.generate_signals(prices)
signals_macd = macd_strat.generate_signals(prices)
signals_mom = mom_strat.generate_signals(prices)
signals_roc = roc_strat.generate_signals(prices)

# Backtesting example
backtester = Backtester(mac, initial_cash=10000)
result = backtester.run(prices)
print("Equity curve:", result["equity_curve"])
print("Max Drawdown:", calc_max_drawdown(result["equity_curve"]))
```

```python
from quanttools.options import (
    black_scholes_call_price,
    black_scholes_put_price,
    black_scholes_call_delta,
    black_scholes_put_delta,
    black_scholes_gamma,
    black_scholes_vega,
    black_scholes_call_theta,
    black_scholes_put_theta,
    black_scholes_call_rho,
    black_scholes_put_rho,
)
from quanttools.strategy import OptionBuyAndHoldStrategy, OptionStraddleStrategy

# Options pricing and Greeks example
S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
call_price = black_scholes_call_price(S, K, T, r, sigma)
put_price = black_scholes_put_price(S, K, T, r, sigma)
call_delta = black_scholes_call_delta(S, K, T, r, sigma)
gamma = black_scholes_gamma(S, K, T, r, sigma)

# Option strategies: buy and hold, straddle on high IV
iv_series = [0.15, 0.18, 0.25, 0.22, 0.15]
obh_strategy = OptionBuyAndHoldStrategy()
straddle_strategy = OptionStraddleStrategy(threshold=0.2)
signals_obh = obh_strategy.generate_signals(iv_series)
signals_straddle = straddle_strategy.generate_signals(iv_series)
```
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

# R / Stan Integration
## Broker Integrations

This framework provides ready-to-use `ExecutionHandler` subclasses for live trading through Robinhood and TD Ameritrade.

### Robinhood

Use the unofficial [`robin_stocks`](https://github.com/jmfernandes/robin_stocks) library:
```bash
poetry add robin_stocks
```
Set your Robinhood credentials in environment variables:
```bash
export ROBINHOOD_USER=<your_username>
export ROBINHOOD_PASS=<your_password>
```
Then instantiate and send orders:
```python
from quanttools.brokers.robinhood import RobinhoodExecutionHandler

handler = RobinhoodExecutionHandler()
# Buy one share
handler.send_order("AAPL", 1)
# Sell one share
handler.send_order("AAPL", -1)
```

### TD Ameritrade

First install the official TD Ameritrade API wrapper:
```bash
poetry add tda-api
```
Register a developer application to obtain an API key and configure OAuth:
```bash
export TDA_API_KEY=<your_api_key>
export TDA_REDIRECT_URI=<your_redirect_uri>
export TDA_ACCOUNT_ID=<your_account_id>
```
Perform the OAuth handshake once (it creates `tda_token.json`), then use:
```python
from quanttools.brokers.tdameritrade import TDAExecutionHandler

handler = TDAExecutionHandler()
# Buy one share
handler.send_order("AAPL", 1)
# Sell one share
handler.send_order("AAPL", -1)
```

# R / Stan Integration

This project includes a simple Bayesian time-series example using **cmdstanr** and Stan.
Stan model files are stored under `models/bayes/`. You can fit a toy AR(1) model in R as follows:

```r
# Install cmdstanr and CmdStan if needed:
# install.packages('cmdstanr')
# cmdstanr::install_cmdstan()

library(cmdstanr)
source('src/r/bayes_ar1.R')
data <- rnorm(100)
fit <- fit_ar1_model(data)
print(fit$summary())
```

Use `renv::restore()` to install R dependencies from `renv.lock`.
