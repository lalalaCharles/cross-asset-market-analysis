import numpy as np
import pandas as pd
import yfinance as yf


def validate_prices(prices, tickers):

    prices = prices.copy()

    if prices.columns.has_duplicates:
        raise ValueError("Duplicate asset columns found.")

    prices = prices.reindex(columns=tickers)

    prices.index = pd.to_datetime(prices.index)

    if prices.empty or prices.index.hasnans:
        raise ValueError("Empty data or invalid dates.")

    if prices.index.has_duplicates:
        raise ValueError("Duplicate dates found.")

    prices = prices.apply(pd.to_numeric, errors="raise")

    if np.isinf(prices.to_numpy()).any():
        raise ValueError("Infinite prices found.")

    missing_assets = prices.columns[
        prices.isna().all()
    ].tolist()

    if missing_assets:
        raise ValueError(f"No valid prices for: {missing_assets}")

    if (prices <= 0).any().any():
        raise ValueError("Non-positive prices require investigation.")

    return prices.sort_index().rename_axis("Date")


def load_prices(path, tickers):
    """Load and validate prices from a saved CSV."""

    prices = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
    )

    return validate_prices(prices, tickers)


def download_prices(tickers, start, end):

    raw = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        auto_adjust=True,
        group_by="column",
        multi_level_index=True,
        keepna=True,
        progress=False,
    )

    if raw is None or raw.empty:
        raise ValueError("No data downloaded.")

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError("Unexpected column structure.")

    prices = raw["Close"]

    return validate_prices(prices, tickers)


def create_quality_report(prices):
    """Summarise price coverage and missing values by asset."""

    return pd.DataFrame({
        "Valid observations": prices.count(),
        "Missing observations": prices.isna().sum(),
        "Missing proportion": prices.isna().mean(),
        "First valid date": prices.apply(
            lambda column: column.first_valid_index()
        ),
        "Last valid date": prices.apply(
            lambda column: column.last_valid_index()
        ),
    })
