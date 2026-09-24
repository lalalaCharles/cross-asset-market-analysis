# Analytical comments

- Sample: 2019-01-02 to 2026-09-11, with 1,933 ETF return observations.

- The daily-rebalanced equal-weight ETF portfolio had a CAGR of 19.86%, annualised volatility of 16.11%, and Sharpe of 1.03 using a 3% annual risk-free assumption.

- Weighted standalone volatility was 20.33%; portfolio volatility was 16.11%. The reduction was 4.22 percentage points (20.8% relative).

- Among the ETFs, GLD had the lowest volatility (17.77%) and QQQ the highest (23.94%). Equal Weight Portfolio had the highest sample Sharpe (1.03) among ETFs and portfolio.

- Portfolio maximum drawdown was -22.97%. One-day historical VaR was 1.57% at 95% and 2.80% at 99%, reported using the loss convention.

- QQQ-on-SPY excess-return beta was 1.160 (HAC 95% CI 1.101–1.219, p<0.001); R-squared was 0.874. Daily alpha was 0.000125 (HAC p=0.302).

- Residual lag-1 autocorrelation was 0.009. This descriptive statistic alone is not a formal whiteness test; residual charts should also be inspected for changing variance and outliers.

- ETF correlations use 1,933 common ETF observations; the five-asset correlation uses 1,859 complete quote-return observations. Different market closing times limit same-day comparisons.

## Limitations

The portfolio excludes futures and FX quotes, which require separate funding, roll and currency conventions. No transaction costs, taxes or slippage are modelled. A constant 3% risk-free rate is an assumption. The saved snapshot's original download metadata is unavailable, so adjusted-price provenance cannot be verified from the CSV alone. CAGR and wealth describe the supplied price series; total-return interpretation depends on its adjustment convention. Historical estimates and daily rebalancing results do not establish future performance.
