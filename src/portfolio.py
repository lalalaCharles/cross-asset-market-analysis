"""Fully invested, long-only portfolios on a complete, common return calendar."""
import numpy as np
import pandas as pd

from .metrics import validate_returns

PORTFOLIO_NAME = "Equal Weight Portfolio"


def validate_return_frame(returns):
    if not isinstance(returns, pd.DataFrame):
        raise TypeError("Expected a returns DataFrame.")
    if returns.empty or returns.columns.has_duplicates:
        raise ValueError("Provide non-empty returns with unique asset columns.")
    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError("Expected a DatetimeIndex.")
    if returns.index.hasnans or returns.index.has_duplicates or not returns.index.is_monotonic_increasing:
        raise ValueError("Return dates must be valid, sorted and unique.")
    for asset in returns:
        validate_returns(returns[asset])
    return returns


def equal_weights(returns):
    """DataFrame -> Series, with asset names as labels."""
    validate_return_frame(returns)
    return pd.Series(1 / returns.shape[1], index=returns.columns, name="Weight")


def aligned_weights(returns, weights):
    validate_return_frame(returns)
    if not isinstance(weights, pd.Series):
        raise TypeError("Weights must be a labelled Series.")
    if weights.index.has_duplicates or set(weights.index) != set(returns.columns):
        raise ValueError("Weights must match the return columns exactly.")
    weights = weights.reindex(returns.columns).astype(float)
    if not np.isfinite(weights).all() or (weights < 0).any():
        raise ValueError("Weights must be finite and non-negative.")
    if not np.isclose(weights.sum(), 1, atol=1e-10, rtol=0):
        raise ValueError("Weights must sum to one.")
    return weights


def portfolio_returns(returns, weights, name=PORTFOLIO_NAME):
    """Constant daily weights imply rebalancing each trading day; no costs."""
    weights = aligned_weights(returns, weights)
    return returns.mul(weights, axis="columns").sum(axis=1, skipna=False).rename(name)


def diversification_analysis(returns, weights, trading_days=252):
    """Compare realised volatility with the perfect-correlation benchmark."""
    if trading_days <= 0:
        raise ValueError("trading_days must be positive.")
    weights = aligned_weights(returns, weights)
    covariance = returns.cov(ddof=1) * trading_days
    standalone_vol = returns.std(ddof=1) * np.sqrt(trading_days)
    benchmark = float(weights @ standalone_vol)
    variance = float(weights @ covariance @ weights)
    portfolio_vol = np.sqrt(max(variance, 0.0))
    realised_vol = portfolio_returns(returns, weights).std(ddof=1) * np.sqrt(trading_days)
    if not np.isclose(portfolio_vol, realised_vol):
        raise ArithmeticError("Covariance and realised portfolio volatility disagree.")
    summary = pd.Series({
        "Weighted standalone volatility": benchmark,
        "Portfolio volatility": portfolio_vol,
        "Volatility reduction (absolute)": benchmark - portfolio_vol,
        "Volatility reduction (relative)": 1 - portfolio_vol / benchmark if benchmark > 0 else np.nan,
        "Diversification ratio": benchmark / portfolio_vol if portfolio_vol > 0 else np.nan,
    }, name="Value")
    # Euler contributions sum to portfolio volatility; contributions can be negative.
    contributions = pd.DataFrame({
        "Weight": weights,
        "Standalone volatility": standalone_vol,
        "Volatility contribution": weights * (covariance @ weights) / portfolio_vol if portfolio_vol > 0 else np.nan,
    })
    return summary, contributions, covariance
