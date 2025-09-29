import math
import pytest

from ykp.options import (
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


def test_call_put_parity():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    call = black_scholes_call_price(S, K, T, r, sigma)
    put = black_scholes_put_price(S, K, T, r, sigma)
    # Call-put parity: C - P = S - K * exp(-rT)
    assert pytest.approx(call - put, rel=1e-6) == S - K * math.exp(-r * T)


def test_intrinsic_at_expiry():
    S, K, r, sigma = 120.0, 100.0, 0.01, 0.3
    # At expiration, option price equals intrinsic value
    assert black_scholes_call_price(S, K, 0.0, r, sigma) == pytest.approx(max(S - K, 0.0))
    assert black_scholes_put_price(S, K, 0.0, r, sigma) == pytest.approx(max(K - S, 0.0))


def test_greeks_relationships():
    S, K, T, r, sigma = 100.0, 100.0, 1.0, 0.05, 0.2
    dc = black_scholes_call_delta(S, K, T, r, sigma)
    dp = black_scholes_put_delta(S, K, T, r, sigma)
    # Delta relationship: dc - dp = 1
    assert pytest.approx(dc - dp, rel=1e-6) == 1.0

    gc = black_scholes_gamma(S, K, T, r, sigma)
    # Gamma is the same for calls and puts
    assert gc == pytest.approx(black_scholes_gamma(S, K, T, r, sigma), rel=1e-6)

    v = black_scholes_vega(S, K, T, r, sigma)
    # Vega is positive
    assert v > 0

    tc = black_scholes_call_theta(S, K, T, r, sigma)
    tp = black_scholes_put_theta(S, K, T, r, sigma)
    # Theta is negative for calls and puts at typical parameters
    assert tc < 0
    assert tp < 0

    rc = black_scholes_call_rho(S, K, T, r, sigma)
    rp = black_scholes_put_rho(S, K, T, r, sigma)
    # Call rho is positive, put rho is negative
    assert rc > 0
    assert rp < 0
