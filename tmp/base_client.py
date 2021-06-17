'''

Abstract API

'''

from abc import ABC, abstractmethod
from threading import Thread

from numpy import array as np_arr
from ..data.database import DataBase


class BaseClient(ABC, Thread):
    
    def __init__(self, options):
        self.db = DataBase()
        
    @abstractmethod
    async def download_history(self, db: DataBase) -> np_arr:
        ...
        
    @abstractmethod
    async def _start_candle_streams() -> None:
        ...
    
    @abstractmethod
    def _parse_candle():  #Only logic related to client
        ...
        
    @abstractmethod
    async def get_all_symbols():
        ...
        
    