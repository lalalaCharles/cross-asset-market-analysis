"""Compare pre-defined stress windows using the project's return conventions."""
import pandas as pd

from .metrics import wealth_and_drawdown
from .portfolio import validate_return_frame


def stress_period_comparison(returns, periods, initial_price_date, benchmark="SPY"):
    """Inclusive return-date windows; first return uses the preceding close.

    Drawdown resets wealth to 1 at that preceding close. Correlation is Pearson
    daily-return correlation within each window, not a causal risk attribution.
    Windows must be covered by the supplied sample; never silently truncate.
    """
    validate_return_frame(returns)
    initial_price_date = pd.Timestamp(initial_price_date)
    if initial_price_date >= returns.index[0]:
        raise ValueError("Initial price date must precede the first return.")
    if benchmark not in returns:
        raise ValueError("Benchmark is absent.")
    rows = []
    for label, (start, end) in periods.items():
        start, end = pd.Timestamp(start), pd.Timestamp(end)
        # A weekend/holiday boundary is allowed, but not an uncovered period.
        if start <= initial_price_date or end > returns.index[-1] or start > end:
            raise ValueError(f"Stress window is not fully covered: {label}")
        sample = returns.loc[start:end]
        if len(sample) < 2:
            raise ValueError(f"At least two returns are required: {label}")
        first_position = returns.index.get_loc(sample.index[0])
        base_date = initial_price_date if first_position == 0 else returns.index[first_position - 1]
        for ticker in returns:
            wealth, drawdown = wealth_and_drawdown(sample[ticker])
            rows.append({
                "Period": label, "Ticker": ticker,
                "Requested start": start.date().isoformat(),
                "Requested end": end.date().isoformat(),
                "Base price date": base_date.date().isoformat(),
                "First return date": sample.index[0].date().isoformat(),
                "Last return date": sample.index[-1].date().isoformat(),
                "Observations": len(sample),
                "Cumulative return": wealth.iloc[-1] - 1,
                "Maximum drawdown": drawdown.min(),
                f"Correlation with {benchmark}": sample[ticker].corr(sample[benchmark]),
            })
    return pd.DataFrame(rows).set_index(["Period", "Ticker"])
