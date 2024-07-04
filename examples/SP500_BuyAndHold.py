import StratLab as sl

bt = sl.Backtest(to_excel=True)
bt.set_default_holding("^spx")
bt.run()

