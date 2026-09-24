# Cross-Asset Analysis: Findings

I compared SPY (US equities), QQQ (Nasdaq-100) and GLD (gold) to see how differently they behaved and whether combining them reduced risk. Brent and GBP/USD provide wider market context but are not part of the portfolio.

## From individual assets to portfolio risk

I first looked at how closely the ETFs moved together. SPY and QQQ had a daily-return correlation of 0.935. The QQQ-on-SPY regression also gave a beta of 1.16, showing greater sensitivity to SPY in this sample. GLD's correlations with SPY and QQQ were much lower, at 0.129 and 0.145. This suggested more scope for diversification than holding the two equity ETFs alone, although I did not test that portfolio comparison directly.

I then combined the three ETFs with one third of capital in each, rebalanced daily. Portfolio volatility was 16.11% a year, compared with 20.33% for the weighted average of their individual volatilities. The difference was 4.22 percentage points. That benchmark represents what volatility would be if all three were perfectly positively correlated; it is not a separate investment portfolio.

Equal investment amounts did not give equal risk contributions: QQQ contributed the most to portfolio volatility. And lower volatility did not remove large losses. Maximum drawdown was 22.97%, while 99% one-day Historical VaR was 2.80%. VaR is a historical daily loss threshold, not the largest possible loss.

Together, these results help identify shared exposures and where portfolio risk is concentrated. They do not establish the best allocation.

## Extending the question to corporate bonds

I also compared LQD (Investment Grade) and HYG (High Yield), with SPY as the equity reference. HYG earned more and moved more closely with equities, but had lower volatility and a smaller maximum drawdown than LQD over the full sample. Their relative losses also changed between the COVID sell-off and 2022. The [Fixed Income summary](FIXED_INCOME_SUMMARY.md) explores why credit quality alone cannot describe overall bond-ETF risk.

## Sample and limits

The main ETF sample covers **2 January 2019–11 September 2026**, with 1,933 daily returns. The five-asset correlation uses 1,859 complete observations. The bond module uses 2015–2025, so its SPY figures answer a different sample-period comparison.

Daily rebalancing excludes dealing costs and taxes. The original cross-asset snapshot has incomplete price-adjustment records, so its returns describe the supplied price series. The bond analysis does not separate rate and spread effects or assess individual issuers. All findings are historical, not forecasts.

[Main notebook](analysis.ipynb) · [Portfolio comparison](outputs/tables/asset_portfolio_comparison.csv) · [Fixed Income notebook](fixed_income.ipynb)
