from setuptools import setup, find_packages

setup(
    name='StratLab',
    version='1.0.20',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'yfinance',
        'matplotlib'
    ],
    author='Robert Stickles',
    author_email='rstickles16@outlook.com',
    description='StratLab is a Python library designed to backtest stock market strategies.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rstickles16/StratLab',
    license='MIT',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)


