# To fold all: cmd+k -> cmd+0
# Make sure each function in conditions is only called once

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime as dt
from . import conditions
from . import indicators
from . import data
from . import holdings
from . import xcel
from . import simulate
from . import backtest_stats
from . import version
from . import plots
from . import user_desktop
__version__ = version.get_version()


class Backtest:
    def __init__(
            self,
            starting_amt: float = 1000,
            start: str='1950-01-01',
            end: str=dt.now(),
            to_excel: bool=False,
            writer_path: str = None,
            offline: str = False,
            offline_io: str = None,
            show_stats: bool = True,
            timer: bool = False,
            show_plot: bool = False
    ) -> None:
        self.writer_path = writer_path
        self.start = start
        self.end = end
        self.df = pd.DataFrame()
        self.download_list = []
        self.study_list = []
        self.conditions = []
        self.default_holding = None
        self.starting_amt = starting_amt
        self.offline = offline
        self.offline_io = offline_io
        self.show_stats = show_stats
        self.timer = timer
        self.show_plot = False
        self.to_excel = to_excel
        
        if self.to_excel is True and writer_path is None:
            desktop = user_desktop.get_desktop_path()
            default_path = f'{desktop}/StratLabBacktest.xlsx'
            self.writer_path = default_path
        

        # Create buckets to report runtime lengths
        x = dt.now()-dt.now()
        self.add_condition_timer = x
        self.add_holding_timer = x
        self.run_simulation_timer = x
        self.run_stats_timer = x
        self.plot_timer = x
        self.write_to_excel_timer = x
        self.save_timer = x
        
        if self.offline is True:
            self.df = pd.read_excel(io=self.offline_io)
    
        # Make a writer for the backtest
        if self.to_excel is True:
            self.writer = pd.ExcelWriter(self.writer_path, engine='xlsxwriter')

    def runtime(
            self,
            runtime_start,
            runtime_end
    ):
        return runtime_end - runtime_start

    def make_offline(
            self
    ):
        self.df = pd.read_excel(io=self.offline)

    def set_default_holding(
            self,
            holding: str=None
    ):
        self.default_holding=holding.upper()

    def download_default_holding(
            self
    ):
        if self.default_holding is not None and self.offline is False:
            data.fetch_data(self.df, self.default_holding, 'Close', self.start, self.end)

    def add_condition(
            self,
            name: str,
            ticker_1: str = None,
            study_1: str = None, 
            ticker_2: str = None,
            study_2: str = None,
            operator: str = None,
            study_1_period: int = None,
            study_2_period: int = None,
            study_1_short_period: int = None,
            study_2_short_period: int = None,
            study_1_long_period: int = None,
            study_2_long_period: int = None,
            study_1_period_type: str = None,
            study_2_period_type: str = None,
            value: float = None
    ) -> dict:
        runtime_start = dt.now()
        condition = conditions.add_condition(
            self_conditions=self.conditions,
            self_downloads=self.download_list,
            self_studies=self.study_list,
            name=name,
            ticker_1=ticker_1,
            study_1=study_1, 
            ticker_2=ticker_2,
            study_2=study_2,
            operator=operator,
            study_1_period=study_1_period,
            study_2_period=study_2_period,
            study_1_short_period=study_1_short_period,
            study_2_short_period=study_2_short_period,
            study_1_long_period=study_1_long_period,
            study_2_long_period=study_2_long_period,
            study_1_period_type=study_1_period_type,
            study_2_period_type=study_2_period_type,
            value=value
        )

        self.conditions = condition['conditions']
        self.study_list = condition['studies']
        self.download_list = condition['downloads']
        new_downloads = condition['new_downloads']
        new_studies = condition['new_studies']

        if self.offline is False:
            if len(new_downloads) > 0:
                for download in new_downloads:
                    self.df = data.fetch_data(
                        self.df,
                        download[0],
                        download[1],
                        self.start,
                        self.end
                    )
            
            if len(new_studies) > 0:
                for study in new_studies:
                    self.df = indicators.add_indicator(
                        df=self.df,
                        ticker=study['ticker'],
                        start=self.start,
                        end=self.end,
                        study=study['study'],
                        period=study['study_period'],
                        dtype=study['period_type'],
                        value=study['value'],
                        short_period=study['short_period'],
                        long_period=study['long_period']
                    )

        self.df = holdings.comparison(
            self.df,
            name,
            ticker_1,
            study_1,
            ticker_2,
            study_2,
            operator,
            study_1_period,
            study_2_period,
            study_1_period_type,
            study_2_period_type,
            value
        )

        self.df['Holding'] = ''

        my_list = list(self.df.columns)
        my_list.sort(reverse=True)
        self.df = self.df.loc[:,my_list]

        runtime_end = dt.now()
        timer = self.runtime(runtime_start, runtime_end)
        self.add_condition_timer = self.add_condition_timer + timer

    def add_holding(
        self,
        conditions: list,
        flags: list,
        holdings_list: list,
        weights: list=None,
        compare_type: str = 'and',
        entry_type: str = 'Close',
        leverage: float = None,
        dca_period: int = 1
    ):
        runtime_start = dt.now()

        # Add holding
        holdings.add_holding(
            self.df,
            conditions,
            flags,
            holdings_list,
            weights,
            compare_type,
            entry_type=entry_type,
            dca_period=dca_period,
            add_leverage=leverage
        )
        
        # Fetch data if not already in frame
        if self.offline is False:
            for holding in holdings_list:
                if f'{str(holding).upper()} {entry_type}' not in self.df.columns:
                    data.fetch_data(
                        self.df,
                        ticker=str(holding).upper(),
                        dtype=entry_type
                    )

            # Add leverage when needed
            if leverage is not None:
                for holding in holdings_list:
                    holdings.add_leverage(
                        df=self.df,
                        ticker=f'{str(holding).upper()}',
                        leverage_ratio=leverage,
                        entry=entry_type
                    )

        runtime_end = dt.now()
        self.add_holding_timer += self.runtime(runtime_start, runtime_end)

    def run_simulation(
            self
    ):
        runtime_start = dt.now()
        self.df = simulate.simulate(
            self.df,
            self.starting_amt,
            self.default_holding
        )
        if 'Date' not in self.df.columns:
            self.df['Date'] = self.df.index
        runtime_end = dt.now()
        self.run_simulation_timer += self.runtime(runtime_start, runtime_end)

    def run_stats(
            self
    ):
        runtime_start = dt.now()
        backtest_stats.run_stats(
            df=self.df,
            starting_amt = self.starting_amt,
            show_stats=self.show_stats
        )
        runtime_end = dt.now()
        self.run_stats_timer += self.runtime(runtime_start, runtime_end)

    def plot(
            self
    ):
        runtime_start = dt.now()
        plots.running_total(
            df=self.df,
            show=self.show_plot,
            writer_path = self.writer_path
        )
        runtime_end = dt.now()
        self.plot_timer += self.runtime(runtime_start, runtime_end)

    def write_to_excel(
        self
    ):
        runtime_start = dt.now()
        self.df.to_excel(self.writer)
        self.writer.book.add_worksheet('Charts')
        self.writer.sheets['Charts'].insert_image('A1', self.writer_path.replace('xlsx', 'png'))
        runtime_end = dt.now()
        self.write_to_excel_timer += self.runtime(runtime_start, runtime_end)

    def save(
            self
    ):
        runtime_start = dt.now()
        self.writer.close()
        runtime_end=dt.now()
        self.save_timer += self.runtime(runtime_start, runtime_end)

    def report_time(
            self
    ):
        print(f'~ RUNTIMES ~')
        print(f'add_condition: {self.add_condition_timer}')
        print(f'add_holding: {self.add_holding_timer}')
        print(f'run_simulation {self.run_simulation_timer}')
        print(f'plot: {self.plot_timer} ')
        print(f'run_stats: {self.run_stats_timer}')
        print(f'write_to_excel {self.write_to_excel_timer}')
        print(f'save {self.save_timer}')
        print('')

    def run(
            self
    ):
        self.download_default_holding()
        self.run_simulation()
        self.plot()

        if self.to_excel is True:
            self.write_to_excel()
            self.save()

        self.run_stats()

        if self.timer is True:
            self.report_time()

