# StratLab
Your one stop shop for backtesting stock market strategies and ideas.
# What is it?
StratLab is a Python library designed to backtest stock market strategies. The library currently uses the yfinance (Yahoo Finance) API as a means for extracting financial data, which is then manipulated utilizing Pandas dataframes and Numpy functions. There are also options to extract the backtested results directly into excel files.
# Installation
StratLab is not currently on PyPi, so pip installation is not available. In the meantime, the recommendation is to:
  1. Download the zip file of the repository to a location on your local machine
  2. Add the package location to your python path using the following methods.

# Set Python Path on a MAC
  Step 1: Open bash profile
  ```bash
  nano ~/.bash_profile
  ```
  Step 2: After the last line of text enter following code:
  ```bash
  export PYTHONPATH="${PYTHONPATH}:{EnterYourPathToStratLabHere}"
  ```
  Make sure to replace {EnterYourPathToStratLabHere} with the actual folder path to the package.
  
# How do you use it?
Step 1: Initialize backtest
```python
import StratLib as sl

bt = sl.Backtest()
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
  name='200 SMA Bullish',
  flags=['True'],
  holdings_list=['^NDX']
)
```

Step 4: Run the backtest
```python
bt.run()

