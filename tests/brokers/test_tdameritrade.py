import os
import pytest

from quanttools.brokers.tdameritrade import TDAExecutionHandler


def test_tda_missing_env(monkeypatch):
    monkeypatch.delenv("TDA_API_KEY", raising=False)
    monkeypatch.delenv("TDA_REDIRECT_URI", raising=False)
    with pytest.raises(RuntimeError):
        TDAExecutionHandler()


def test_tda_client_from_token(monkeypatch):
    auth_mod = pytest.importorskip("tda.auth")
    fake_client = object()

    def fake_client_from_token_file(token_path, api_key, redirect_uri):
        assert token_path == "tda_token.json"
        assert api_key == "key"
        assert redirect_uri == "uri"
        return fake_client

    monkeypatch.setattr(auth_mod, "client_from_token_file", fake_client_from_token_file)
    monkeypatch.setenv("TDA_API_KEY", "key")
    monkeypatch.setenv("TDA_REDIRECT_URI", "uri")

    handler = TDAExecutionHandler()
    assert handler._client is fake_client


def test_tda_send_order_market(monkeypatch):
    auth_mod = pytest.importorskip("tda.auth")
    equities_mod = pytest.importorskip("tda.orders.equities")

    # stub auth
    fake_client = type("Client", (), {})()
    called = []

    def fake_client_from_token_file(token_path, api_key, redirect_uri):
        return fake_client

    monkeypatch.setattr(auth_mod, "client_from_token_file", fake_client_from_token_file)
    monkeypatch.setenv("TDA_API_KEY", "key")
    monkeypatch.setenv("TDA_REDIRECT_URI", "uri")
    monkeypatch.setenv("TDA_ACCOUNT_ID", "acct")

    # stub equities
    monkeypatch.setattr(equities_mod, "equity_buy_market", lambda sym, qty: f"buy:{sym}:{qty}")
    monkeypatch.setattr(equities_mod, "equity_sell_market", lambda sym, qty: f"sell:{sym}:{qty}")

    # stub place_order
    def fake_place_order(account_id, order_spec):
        called.append((account_id, order_spec))

    setattr(fake_client, "place_order", fake_place_order)

    handler = TDAExecutionHandler()
    handler.send_order("AAPL", 5, order_type="market")
    handler.send_order("AAPL", -2, order_type="market")

    assert ("acct", "buy:AAPL:5") in called
    assert ("acct", "sell:AAPL:2") in called
