import os
import pytest

from quanttools.brokers.robinhood import RobinhoodExecutionHandler


def test_robinhood_missing_env(monkeypatch):
    monkeypatch.delenv("ROBINHOOD_USER", raising=False)
    monkeypatch.delenv("ROBINHOOD_PASS", raising=False)
    with pytest.raises(RuntimeError):
        RobinhoodExecutionHandler()


def test_robinhood_login_and_send(monkeypatch):
    robin = pytest.importorskip("robin_stocks")
    called = []

    def fake_login(u, p):
        called.append(("login", u, p))

    monkeypatch.setenv("ROBINHOOD_USER", "user")
    monkeypatch.setenv("ROBINHOOD_PASS", "pass")
    monkeypatch.setattr(robin, "login", fake_login)

    # Prepare fake order functions
    def fake_buy(sym, qty):
        called.append(("buy", sym, qty))

    def fake_sell(sym, qty):
        called.append(("sell", sym, qty))

    monkeypatch.setattr(robin.orders, "order_buy_market", fake_buy)
    monkeypatch.setattr(robin.orders, "order_sell_market", fake_sell)

    handler = RobinhoodExecutionHandler()
    assert ("login", "user", "pass") in called

    handler.send_order("AAPL", 2, order_type="market")
    handler.send_order("AAPL", -3, order_type="market")
    assert ("buy", "AAPL", 2) in called
    assert ("sell", "AAPL", 3) in called

    with pytest.raises(NotImplementedError):
        handler.send_order("AAPL", 1, order_type="limit")
