"""Small deterministic checks for the financial conventions and failure cases."""
import unittest
import numpy as np
import pandas as pd
from src.metrics import wealth_and_drawdown, historical_var, calculate_metrics
from src.portfolio import equal_weights, portfolio_returns, diversification_analysis


class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.r = pd.DataFrame({"A": [-0.1, 0.1, 0.02], "B": [0.1, -0.1, -0.02]}, index=pd.date_range("2020-01-02", periods=3))

    def test_label_alignment_and_rebalancing(self):
        w = pd.Series({"B": 0.25, "A": 0.75})
        np.testing.assert_allclose(portfolio_returns(self.r, w), [-0.05, 0.05, 0.01])

    def test_perfect_hedge(self):
        d, c, cov = diversification_analysis(self.r, equal_weights(self.r))
        self.assertAlmostEqual(d["Portfolio volatility"], 0)
        self.assertAlmostEqual(d["Volatility reduction (relative)"], 1)
        self.assertTrue(np.isnan(d["Diversification ratio"]))

    def test_perfect_correlation_no_benefit(self):
        r = self.r.assign(B=self.r.A * 2)
        d, c, _ = diversification_analysis(r, equal_weights(r))
        self.assertAlmostEqual(d["Volatility reduction (absolute)"], 0)
        self.assertAlmostEqual(c["Volatility contribution"].sum(), d["Portfolio volatility"])

    def test_missing_values_rejected(self):
        r = self.r.copy(); r.iloc[0, 0] = np.nan
        with self.assertRaises(ValueError):
            portfolio_returns(r, pd.Series({"A": .5, "B": .5}))

    def test_invalid_weights_rejected(self):
        for w in [pd.Series({"A": .5, "C": .5}), pd.Series({"A": .5, "B": .6}), pd.Series({"A": 2., "B": -1.})]:
            with self.assertRaises(ValueError):
                portfolio_returns(self.r, w)

    def test_initial_capital_is_peak(self):
        _, dd = wealth_and_drawdown(self.r.A)
        self.assertAlmostEqual(dd.iloc[0], -.1)

    def test_var_and_sharpe_conventions(self):
        self.assertAlmostEqual(historical_var(self.r.A), .088)
        m = calculate_metrics(self.r.A, pd.Timestamp("2020-01-01"), annual_rf=0)
        expected = self.r.A.mean() / self.r.A.std(ddof=1) * np.sqrt(252)
        self.assertAlmostEqual(m["Sharpe"], expected)


if __name__ == "__main__":
    unittest.main()
