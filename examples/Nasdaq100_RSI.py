import StratLab as sl

# Initialize backtest
bt = sl.Backtest(to_excel=True)

# Add condition for when ^NDX (Nasdaq 100) is above its 200D moving average
bt.add_condition(
    name='Oversold',
    ticker_1='^NDX',
    study_1='rsi',
    study_1_period=10,
    operator='<',
    value=10
)

# Add holding for when condition is true
bt.add_holding(
    conditions=['Oversold'],
    flags=['True'],
    holdings_list=['^NDX']
)

# Run backtest
bt.run()