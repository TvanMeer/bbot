from typing import List, Set
from typeguard import typechecked

from ..options   import Options
from .candle     import Candle
from .pair       import Pair
from .user_event import UserEvent

@typechecked
class Database:
    """Holds all Pairs with k = symbol and v = Pair object.
    Also holds user_event objects in an array.
    """

    def __init__(self, options: Options):
        self.options          = options
        self.all_symbols      = None
        self.selected_symbols = None
        self.pairs            = {}
        self.user_events      = []


    def _filter_symbols(self, symbols: Set) -> Set:
        """Filters all symbols and returns symbols that have both
        base and quote assets listed in Options.base_assets and 
        Options.quote_assets.
        """

        filtered = set()
        for qa in self.options.quote_assets:
            for s in symbols:
                if s.endswith(qa):
                    starts_with = s[:-len(qa)]
                    if starts_with in self.options.base_assets:
                        filtered.add(s)
        
        self._create_pairs(symbols, filtered)
        return frozenset(filtered)


    def _create_pairs(self, all_symbols: Set, selected_symbols: Set) -> None:
        
        self.all_symbols = frozenset(all_symbols)
        self.selected_symbols = frozenset(selected_symbols)
        for s in selected_symbols:
            self.pairs[s] = Pair(self.options)


    def _process_user_event(self, user_event: UserEvent) -> None:
        #...
        self.user_events.append(user_event)
        self._update_gui_user_event(user_event)

    def _update_gui_user_event(self, user_event: UserEvent) -> None:
        pass


