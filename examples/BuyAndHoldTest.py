import StratLab as sl

bt = sl.Backtest(to_excel=True, include_plot=False)
bt.set_default_holding("^spx")
bt.run()