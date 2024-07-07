import StratLab as sl

# Initialize backtest
bt = sl.Backtest(to_excel=True)

# Add condition for when ^NDX (Nasdaq 100) is above its 200D moving average
bt.add_condition(
    name='MACD Bullish',
    ticker_1='^NDX',
    study_1='macd',
    study_1_period=9,
    study_1_short_period=13,
    study_1_long_period=26,
    operator='>',
    value=0
)

# Add holding for when condition is true
bt.add_holding(
    conditions=['MACD Bullish'],
    flags=['True'],
    holdings_list=['^NDX']
)

# Run backtest
bt.run()