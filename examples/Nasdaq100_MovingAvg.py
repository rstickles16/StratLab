import StratLab as sl

# Initialize backtest
bt = sl.Backtest(to_excel=True)

# Add condition for when ^NDX (Nasdaq 100) is above its 200D moving average
bt.add_condition(
    name='200 MA Bullish',
    ticker_1='^NDX',
    study_1='price',
    operator='>',
    ticker_2='^NDX',
    study_2='sma',
    study_2_period=200
)

# Add holding for when condition is true
bt.add_holding(
    conditions=['200 MA Bullish'],
    flags=['True'],
    holdings_list=['^NDX']
)

# Run backtest
bt.run()