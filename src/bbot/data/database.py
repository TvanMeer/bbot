from typing import FrozenSet

from ..options import Options
from .pair import _Pair
from .user_event import UserEvent


# @typechecked
class Database:
    """Holds all pairs with k = symbol and v = _Pair object.
    Also holds user_event objects in an array.
    """

    def __init__(self, options: Options):
        self.options = options
        self.all_symbols = None
        self.selected_symbols = None
        self.pairs = {}
        self.user_events = []

    def _filter_symbols(self, symbols: FrozenSet) -> FrozenSet:
        """Filters all symbols and returns symbols that have both
        base and quote assets listed in Options.base_assets and
        Options.quote_assets.
        """

        filtered = set()
        for qa in self.options.quote_assets:
            for s in symbols:
                if s.endswith(qa):
                    starts_with = s[: -len(qa)]
                    if starts_with in self.options.base_assets:
                        filtered.add(s)

        self.create_pairs(symbols, filtered)
        return frozenset(filtered)

    def create_pairs(
        self, all_symbols: FrozenSet, selected_symbols: FrozenSet
    ) -> None:

        self.all_symbols = frozenset(all_symbols)
        self.selected_symbols = frozenset(selected_symbols)
        for s in self.selected_symbols:
            self.pairs[s] = _Pair(s, self.options)

    def process_user_event(self, user_event: UserEvent) -> None:

        # ... TODO
        self.user_events.append(user_event)
        self.update_gui_user_event(user_event)

    def update_gui_user_event(self, user_event: UserEvent) -> None:

        pass  # TODO
