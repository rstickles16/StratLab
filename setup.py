from setuptools import setup, find_packages

setup(
    name='StratLab',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'yfinance'
    ],
    author='Robert Stickles',
    author_email='rstickles16@outlook.com',
    description='Description of your package',
    url='https://github.com/rstickles16/StratLab',
)
