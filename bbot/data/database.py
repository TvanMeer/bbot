'''

Database class: holds all Pairs.

'''
from typing import Dict, List, Set

from .. import options

class Database:
    def __init__(self, options: options.Options):
        self.options = options

    def _filter_symbols(self, symbols: Set) -> Set:
        
        filtered = Set() #...
        self._create_pairs(filtered)
        return filtered

    def _create_pairs(self, symbols: Set) -> None:
        pass

    def _route_history(self, history: List[Dict[str, float]]) -> None:
        pass

    def _route_candle(self, candle: Dict[str, float]) -> None:
        pass

    def _process_user_event(self, user_event: Dict) -> None:
        #...
        self._update_gui_user_event(user_event)

    def _update_gui_user_event(self, user_event: Dict) -> None:
        pass


