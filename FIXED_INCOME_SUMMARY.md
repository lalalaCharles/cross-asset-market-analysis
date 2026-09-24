# Investment Grade and High Yield: Findings

I compared LQD (Investment Grade corporate bonds) and HYG (High Yield corporate bonds) to see whether HYG earned more and carried more risk. I included SPY to check how closely each bond ETF moved with equities.

## Return, risk and market conditions

I started with the full sample. HYG returned 4.44% a year, compared with 2.73% for LQD, measured by CAGR. But HYG was not riskier on every measure: its annualised volatility was slightly lower (8.31% versus 8.45%), and its maximum drawdown was smaller (22.03% versus 24.95%). Its 99% one-day Historical VaR was higher, at 1.43% versus 1.35%. VaR measures a daily loss threshold, while drawdown measures a fall from a previous peak, so they need not rank the ETFs in the same order.

I then checked their relationship with equities. HYG's daily-return correlation with SPY was 0.768, compared with 0.270 for LQD. HYG therefore moved more closely with equities over this sample.

To put these averages in context, I compared selected stress periods. During the COVID sell-off, HYG lost 21.90% and LQD 12.30%. In 2022, LQD lost more: 17.92%, against 10.98% for HYG. This shows why I would look at interest-rate sensitivity alongside credit quality when reviewing bond exposure. I would need historical duration and spread data to explain the difference more clearly.

## Sample and limits

The sample covers **2 January 2015–31 December 2025**, with 2,765 daily returns per ETF. Yahoo Finance adjusted prices, downloaded on 23 September 2026, are a USD total-return proxy, not official NAV performance. Missing prices stop the analysis. Exact stress dates and methods are in the [notebook](fixed_income.ipynb).

Both ETFs carry interest-rate and credit-spread risk and differ in duration, holdings, sectors and credit quality. These results do not isolate credit risk. Stress windows were chosen retrospectively and differ in length. Fund expenses are reflected in prices; investor dealing costs and taxes are excluded. This is ETF analysis, not issuer-level credit analysis: it does not establish relative value, identify a cheap bond or forecast performance.

[Return and risk](outputs/fixed_income/tables/performance_comparison.csv) · [Stress periods](outputs/fixed_income/tables/stress_period_comparison.csv) · [Data provenance](data/fixed_income_metadata.json)
