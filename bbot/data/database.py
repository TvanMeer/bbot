'''

Database class: holds all Pairs.

'''
from typing import Dict, List, Set

from ..options import Options
from .candle   import Candle

class Database:
    def __init__(self, options: Options):
        self.options = options

    def _filter_symbols(self, symbols: Set) -> Set:
        
        filtered = Set() #...
        self._create_pairs(filtered)
        return filtered

    def _create_pairs(self, symbols: Set) -> None:
        pass

    def _route_history(self, history: List[Candle]) -> None:
        pass

    def _route_candle(self, candle: Candle) -> None:
        pass

    def _process_user_event(self, user_event: Dict) -> None:
        #...
        self._update_gui_user_event(user_event)

    def _update_gui_user_event(self, user_event: Dict) -> None:
        pass


