# What is StratLab?
StratLab is a Python library designed to backtest stock market strategies. The library currently uses the yfinance (Yahoo Finance) API as a means for extracting financial data, which is then manipulated utilizing Pandas dataframes and Numpy functions. There are also options to extract the backtested results directly into excel files.
# How do you install it?
Run the following command in your terminal
```bash
pip install StratLab
```
# How do you use it?
Step 1: Initialize backtest
```python
# This imports the StratLab library and intializes the Backtest.
# The to_excel argument writes an excel file to your desktop with an analysis of the backtest.
import StratLib as sl

bt = sl.Backtest(to_excel=True)
```
Step 2: Add condition for trade
```python
# This example creates a condition in the backtest for when
# ^NDX (Nasdaq 100 Index) price is above its 200D moving average...
bt.add_condition(
  name='200 SMA Bullish',
  ticker_1='^NDX',
  study_1='price',
  operator='>',
  ticker_2='^NDX',
  study_2='sma',
  study_2_period=200
)
```

Step 3: Add holding for the condition(s)
```python
# This example tells the backtest to hold ^NDX (Nasdaq 100 Index)
# when the "200 SMA Bullish" condition is True...
bt.add_holding(
  conditions=['200 SMA Bullish'],
  flags=['True'],
  holdings_list=['^NDX']
)
```

Step 4: Run the backtest
```python
bt.run()

