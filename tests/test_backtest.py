from ykp.strategy import MovingAverageCrossStrategy
from ykp.backtest import Backtester


def test_backtest_run():
    prices = [1, 2, 3, 4, 3, 2]
    strat = MovingAverageCrossStrategy(2, 3)
    backtester = Backtester(strat, initial_cash=10)
    result = backtester.run(prices)
    assert "equity_curve" in result
    assert "returns" in result
    assert len(result["equity_curve"]) == len(prices)
    assert len(result["returns"]) == len(prices) - 1
