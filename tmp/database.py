'''

All data is loaded in memory and contained in single class database

'''
from ..options import Options
from .pair import Pair

class Pairs():
    # Iterator
    ...

class DataBase():
    
    def __init__(self, options: Options) -> None:
        self.options          = options
        self.all_symbols      = None
        self.selected_symbols = None
        self.pairs = Pairs()
        self.
        
    @property
    def all_pairs(self):
        return self.Pairs()
    
    @all_pairs.setter
    def _all_pairs(self):
        ...
        
    def _set_all_symbols = ''
    
    def _select_symbols(self, raw):
        pass