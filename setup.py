from setuptools import setup, find_packages

setup(
    name='StratLab',
    version='1.0.9',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'yfinance',
        'matplotlib'
    ],
    author='Robert Stickles',
    author_email='rstickles16@outlook.com',
    description='StratLab is a Python library designed to backtest stock market strategies. The library currently uses the yfinance (Yahoo Finance) API as a means for extracting financial data, which is then manipulated utilizing Pandas dataframes and Numpy functions. There are also options to extract the backtested results directly into excel files.',
    url='https://github.com/rstickles16/StratLab',
)
