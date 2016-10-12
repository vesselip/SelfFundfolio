# SelfFundfolio
Python NumPy/Pandas backtesting app for simulation of stradle self funded strategies.

This stratgey is implemented like so:

- every Friday we sell 25 business day maturity ATM Europeans straddle for 25% of the strategy reference notional, input trade is delta neutral
- strike rounded to nearest 10 on SPX to closing spot. Invested amount at time of trading should never be above 100% of reference notional.
- Portfolio hedge is adjusted to be delta neutral at EoD (hedge is cash spot)
- ITM Option are cash settled against EoD spot on day of expiry
- Daily report should show: Cash Account, Portfolio Composition, Gamma, Vega, Theta, Total Portfolio Value
- PnL is reinvested in strategy. Profit increases and loss reduce strategy reference notional.

For Black-Scholes:
•	IR are constant (input to the strategy)
•	No Skew or smile, only use ATM vol for valuing options
•	No dividend
•	No slippage on trades (options and future)
•	No cost for trading

Data:
•	2 year time series for .SPX
•	Date, maturity, Spot, ATM volatility

In the end we generate report to show whether the strategy is profitable together with PnL profile etc
