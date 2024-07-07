import StratLab as sl

# Initialize backtest
bt = sl.Backtest(to_excel=True)

# Add condition for when ^NDX (Nasdaq 100) is above its 200D moving average
bt.add_condition(
    name='200 SMA Deviation',
    ticker_1='^NDX',
    study_1='smadeviation',
    study_1_period=200,
    operator='>',
    value=.01
)

# Add holding for when condition is true
bt.add_holding(
    conditions=['200 SMA Deviation'],
    flags=['True'],
    holdings_list=['^NDX'],
    leverage=3
)

# Run
bt.run()