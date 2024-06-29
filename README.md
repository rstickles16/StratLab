# QuantLab
# What is it?
QuantLab is a Python library designed to backtest stock market strategies. The library currently uses the yfinance (Yahoo Finance) API as a means for extracting financial data, which is then manipulated utilizing Pandas dataframes and Numpy functions. There are also options to extract the backtested results directly into excel files.
# How do you use it?
Step 1: Initialize backtest
```python
bt = Backtest()
```
Step 2: Add condition for trade
```python
bt.add_condition(
  name='200 SMA Bullish',
  ticker_1='^NDX',
  study_1='price',
  operator='>',
  ticker_2='^NDX',
  study_2='sma',
  study_2_period=200
)

Step 3: Add holding for the condition(s)
```python
bt.add_holding(
  name='200 SMA Bullish',
  flags=['True'],
  holdings_list=['^NDX']
)
```

Step 4: Run the backtest
```python
bt.run()

