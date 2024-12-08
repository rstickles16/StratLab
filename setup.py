from setuptools import setup, find_packages
import os

version = '1.0.23'

# Get the current folder path of this script
current_folder = os.path.dirname(os.path.abspath(__file__))

# Send version to the package
with open(f'{current_folder}/StratLab/__vrsn__.txt', 'w') as file:
    file.write(version)


setup(
    name='StratLab',
    version=version,
    packages=find_packages(where='.'),
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


