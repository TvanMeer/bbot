'''

A single window, such as bbot.BTCUSDT.m15

'''
from os import path
from typing import Dict, List
from numpy import array as np_array
from pandas import DataFrame

from .options import Interval
from .info import Info


class Window():
    
    # Type aliases
    HistCandles  = list[list[str]]
    RawCandle    = dict[str, str]
    ParsedCandle = dict[str, float]

    def __init__(self, interval: Interval, n_rows = int) -> None:

        self.interval = interval
        self.n_rows   = n_rows
        self.candles  = []
    
    @property
    def last(self, n=1):
        return self.candles[-n]

    @property
    def first(self, n=1):
        return self.candles[n-1]

    def as_dicts(self) -> List[Dict[str, float]]:
        '''Returns self.candles as list of dicts'''
        return self.candles

    def as_np(self) -> np_array:
        '''Returns self.candles as numpy array'''
        pass

    def as_df(self) -> DataFrame:
        '''Returns self.candles as Pandas DataFrame'''
        pass

    def pretty(self) -> str:
        '''Returns clean indented JSON string'''
        pass

    def save_as_json(self, target: path) -> bool:
        '''Writes data to disk as indented JSON'''
        pass

    def save_as_csv(self, target: path) -> bool:
        '''Writes data to disk as CSV-file'''
        pass
    
    
    # Internal functions to handle historical candles ------------------
    def _insert_history(self, )

    # Internal functions to handle streams
    def _insert_new_candle(self, c: ParsedCandle) -> None:
        '''Pipeline for inserting a single new candle from a websocket'''

        vc = self._verify_new_candle(c)
        self._execute_insert(vc)
    
    def _update_last_candle(self, c: ParsedCandle) -> None:
        '''Pipeline for updating the last candle through a websocket'''
        
        vc = self._verify_update(c)
        self._execute_update(vc)
    
    
    
    def _verify_new_candle(self, c: ParsedCandle) -> ParsedCandle:
        '''Verify data integrity of incoming candle'''
        pass
    
    def _execute_insert(self, c: ParsedCandle) -> None:
        pass
    
    
    def _verify_update(self, c: ParsedCandle) -> ParsedCandle:
        '''Verify data integrity of last candle update'''
        pass
    
    def _execute_update(self, c: ParsedCandle) -> None:
        '''Update the last candle in self.candles'''
        pass