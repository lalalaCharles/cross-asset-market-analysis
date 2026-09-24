import numpy as np
import pandas as pd


def validate_returns(returns):
    """Validate a complete finite return Series."""

    if not isinstance(returns, pd.Series):
        raise TypeError("Expected a pandas Series.")

    if len(returns) < 2:
        raise ValueError("At least two returns are required.")

    if not np.isfinite(returns.to_numpy()).all():
        raise ValueError("Returns contain missing or infinite values.")

    if (returns <= -1).any():
        raise ValueError("This implementation requires returns > -100%.")

    return returns


def wealth_and_drawdown(returns):
    """Calculate compounded wealth and drawdown from daily returns."""

    returns = validate_returns(returns)

    wealth = (1 + returns).cumprod()

    # Include initial capital as a possible running peak.
    peak = wealth.cummax().clip(lower=1.0)

    drawdown = wealth / peak - 1

    return wealth, drawdown


def historical_var(returns, confidence=0.95):
    """Historical VaR: negative lower-tail return quantile, linearly interpolated."""

    returns = validate_returns(returns)

    if not 0.5 < confidence < 1:
        raise ValueError("Confidence must be between 0.5 and 1.")

    return_quantile = returns.quantile(
        1 - confidence,
        interpolation="linear",
    )

    return -return_quantile


def calculate_metrics(
    returns,
    start_date,
    annual_rf=0.03,
    trading_days=252,
):
    """Calculate performance and risk metrics for one return Series."""

    returns = validate_returns(returns)

    if not isinstance(returns.index, pd.DatetimeIndex):
        raise TypeError("Returns must have a DatetimeIndex.")

    if (
        not returns.index.is_monotonic_increasing
        or returns.index.has_duplicates
    ):
        raise ValueError("Return dates must be sorted and unique.")

    start_date = pd.Timestamp(start_date)

    if start_date >= returns.index[0]:
        raise ValueError("start_date must precede the first return date.")

    wealth, drawdown = wealth_and_drawdown(returns)

    years = (
        returns.index[-1] - start_date
    ).days / 365.25

    total_return = wealth.iloc[-1] - 1

    annualised_return = (
        wealth.iloc[-1] ** (1 / years) - 1
    )

    daily_volatility = returns.std(ddof=1)

    daily_rf = (
        (1 + annual_rf) ** (1 / trading_days) - 1
    )

    sharpe = (
        (returns.mean() - daily_rf)
        / daily_volatility
        * np.sqrt(trading_days)
        if daily_volatility > 0
        else np.nan
    )

    return pd.Series({
        "Observations": len(returns),
        "Cumulative return": total_return,
        "Annualised return": annualised_return,
        "Annualised volatility": (
            daily_volatility * np.sqrt(trading_days)
        ),
        "Sharpe": sharpe,
        "Maximum drawdown": drawdown.min(),
        "Historical VaR 95%": historical_var(returns, 0.95),
        "Historical VaR 99%": historical_var(returns, 0.99),
    })

def comparison_metrics(returns, start_date, annual_rf=0.03, trading_days=252):
    """DataFrame -> one metric row per asset/portfolio on the same sample."""
    from .portfolio import validate_return_frame

    validate_return_frame(returns)
    return returns.apply(
        calculate_metrics, start_date=start_date,
        annual_rf=annual_rf, trading_days=trading_days,
    ).T
