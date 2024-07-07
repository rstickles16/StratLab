import StratLab as sl

# Initialize backtest
bt = sl.Backtest(to_excel=True)

# Add condition for when ^NDX (Nasdaq 100) is above its 200D moving average
bt.add_condition(
    name='SAR Bullish',
    ticker_1='^NDX',
    study_1='price',
    operator='>',
    ticker_2='^NDX',
    study_2='sar'
)

# Add holding for when condition is true
bt.add_holding(
    conditions=['SAR Bullish'],
    flags=['True'],
    holdings_list=['^NDX']
)

# Run
bt.run()