"""Stress-window boundary and failure checks, independent of market data."""
import unittest
import numpy as np
import pandas as pd
from src.fixed_income import stress_period_comparison


class StressPeriodTests(unittest.TestCase):
    def setUp(self):
        self.returns = pd.DataFrame(
            {"LQD": [.05, -.10, .02, .03], "SPY": [.02, -.20, .05, .01]},
            index=pd.to_datetime(["2020-01-02", "2020-01-03", "2020-01-06", "2020-01-07"]))

    def test_includes_first_day_return_and_preceding_close(self):
        result = stress_period_comparison(self.returns,
            {"test": ("2020-01-03", "2020-01-06")}, "2019-12-31")
        row = result.loc[("test", "LQD")]
        self.assertAlmostEqual(row["Cumulative return"], .90 * 1.02 - 1)
        self.assertAlmostEqual(row["Maximum drawdown"], -.10)
        self.assertEqual(row["Base price date"], "2020-01-02")
        self.assertEqual(row["Observations"], 2)

    def test_benchmark_label_matches_selected_series(self):
        result = stress_period_comparison(self.returns,
            {"test": ("2020-01-02", "2020-01-07")}, "2019-12-31", benchmark="LQD")
        self.assertIn("Correlation with LQD", result.columns)
        self.assertNotIn("Correlation with SPY", result.columns)
        self.assertAlmostEqual(result.loc[("test", "LQD"), "Correlation with LQD"], 1.0)

    def test_weekend_start_uses_last_trading_close(self):
        result = stress_period_comparison(self.returns,
            {"test": ("2020-01-04", "2020-01-07")}, "2019-12-31")
        self.assertEqual(result.loc[("test", "LQD"), "Base price date"], "2020-01-03")

    def test_missing_prices_do_not_become_zero_returns(self):
        prices = pd.Series([100., np.nan, 102., 103.])
        changes = prices.pct_change(fill_method=None)
        self.assertTrue(changes.iloc[1:3].isna().all())
        bad = self.returns.copy()
        bad.iloc[1, 0] = np.nan
        with self.assertRaises(ValueError):
            stress_period_comparison(bad, {"test": ("2020-01-02", "2020-01-07")}, "2019-12-31")

    def test_rejects_truncated_and_too_short_windows(self):
        for start, end in [("2019-12-01", "2020-01-07"),
                           ("2020-01-02", "2020-01-08"),
                           ("2020-01-07", "2020-01-07")]:
            with self.assertRaises(ValueError):
                stress_period_comparison(self.returns, {"test": (start, end)}, "2019-12-31")


if __name__ == "__main__":
    unittest.main()
