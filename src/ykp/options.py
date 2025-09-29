"""
Module for option pricing and greeks using the Black-Scholes model.
"""

import math


def _norm_pdf(x: float) -> float:
    """Probability density function of the standard normal distribution."""
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def _norm_cdf(x: float) -> float:
    """Cumulative distribution function of the standard normal distribution."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def black_scholes_call_price(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """
    Compute the Black-Scholes price of a European call option.

    :param S: Current underlying price.
    :param K: Strike price.
    :param T: Time to expiration in years.
    :param r: Risk-free interest rate (annualized).
    :param sigma: Volatility of the underlying (annualized).
    :returns: Call option price.
    """
    if T == 0:
        return max(S - K, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)


def black_scholes_put_price(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """
    Compute the Black-Scholes price of a European put option.

    :param S: Current underlying price.
    :param K: Strike price.
    :param T: Time to expiration in years.
    :param r: Risk-free interest rate (annualized).
    :param sigma: Volatility of the underlying (annualized).
    :returns: Put option price.
    """
    if T == 0:
        return max(K - S, 0.0)
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def black_scholes_call_delta(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the delta of a European call option under Black-Scholes."""
    if T == 0:
        return 1.0 if S > K else 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return _norm_cdf(d1)


def black_scholes_put_delta(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the delta of a European put option under Black-Scholes."""
    if T == 0:
        return -1.0 if S < K else 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return _norm_cdf(d1) - 1


def black_scholes_gamma(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the gamma of a European option under Black-Scholes."""
    if T == 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return _norm_pdf(d1) / (S * sigma * math.sqrt(T))


def black_scholes_vega(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the vega of a European option under Black-Scholes."""
    if T == 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    return S * _norm_pdf(d1) * math.sqrt(T)


def black_scholes_call_theta(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the theta of a European call option under Black-Scholes."""
    if T == 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    term1 = -S * _norm_pdf(d1) * sigma / (2 * math.sqrt(T))
    term2 = -r * K * math.exp(-r * T) * _norm_cdf(d2)
    return term1 + term2


def black_scholes_put_theta(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the theta of a European put option under Black-Scholes."""
    if T == 0:
        return 0.0
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    term1 = -S * _norm_pdf(d1) * sigma / (2 * math.sqrt(T))
    term2 = r * K * math.exp(-r * T) * _norm_cdf(-d2)
    return term1 + term2


def black_scholes_call_rho(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the rho of a European call option under Black-Scholes."""
    if T == 0:
        return 0.0
    d2 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T)) - sigma * math.sqrt(T)
    return K * T * math.exp(-r * T) * _norm_cdf(d2)


def black_scholes_put_rho(
    S: float, K: float, T: float, r: float, sigma: float
) -> float:
    """Compute the rho of a European put option under Black-Scholes."""
    if T == 0:
        return 0.0
    d2 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T)) - sigma * math.sqrt(T)
    return -K * T * math.exp(-r * T) * _norm_cdf(-d2)
