import StratLab as sl

bt = sl.Backtest(timer=True)
bt.add_condition(
    name='long_sma',
    ticker_1='qqq',
    study_1='price',
    operator='>',
    ticker_2='qqq',
    study_2='sma',
    study_2_period=200
)

bt.add_holding(
    ['long_sma'], [True], ['qqq']
)

bt.run()