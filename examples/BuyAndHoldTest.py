import StratLab as sl

# Module below should run a buy and hold backtest, export it to excel,
# and display the plot both in the terminal and the excel file

bt = sl.Backtest(to_excel=True, show_plot=False)
bt.set_default_holding("^spx")
bt.run()
print(bt.stats)