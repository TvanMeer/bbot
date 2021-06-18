'''

Database class: holds all Pairs.

'''

from typing import List, Set
from typeguard import typechecked

from ..options   import Options
from .candle     import Candle
from .pair       import Pair
from .user_event import UserEvent

@typechecked
class Database:
    def __init__(self, options: Options):
        self.options     = options
        self.pairs       = {}
        self.user_events = []

    def _filter_symbols(self, symbols: Set) -> Set:
        
        filtered = Set() #...
        self._create_pairs(filtered)
        return filtered

    def _create_pairs(self, symbols: Set) -> None:
        for s in symbols:
            self.pairs[s] = Pair(self.options)


    def _route_history(self, history: List[Candle]) -> None:
        pass

    def _route_candle(self, candle: Candle) -> None:
        pass

    def _process_user_event(self, user_event: UserEvent) -> None:
        #...
        self.user_events.append(user_event)
        self._update_gui_user_event(user_event)

    def _update_gui_user_event(self, user_event: UserEvent) -> None:
        pass


