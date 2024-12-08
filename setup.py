from setuptools import setup, find_packages
import os

# Get the current folder path of this script
current_folder = os.path.dirname(os.path.abspath(__file__))

# Send version to the package
with open(f'{current_folder}/StratLab/__vrsn__.txt', 'r') as file:
    version = file.read()


print(f'Running setup of StratLab version {version}')

setup(
    name='StratLab',
    version=version,
    packages=find_packages(where='.'),
    install_requires=[
        'datetime',
        'pandas',
        'numpy',
        'yfinance',
        'matplotlib'
    ],
    author='Robert Stickles',
    author_email='rstickles16@outlook.com',
    description='Python library dedicated to simplifying the process of backtesting complex stock market strategies.',
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


