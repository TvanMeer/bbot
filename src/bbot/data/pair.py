from typing import FrozenSet

from ..options import Options
from .window import Window
from .candle import Candle


class _Pair:
    """Holds all windows and additional data related to a single pair,
    like BTCUSDT.
    """

    def __init__(self, symbol, options: Options) -> None:
        self.symbol = symbol
        self.windows = {}

        for iv, ws in options.windows.items():
            self.windows[symbol] = Window(iv, ws)

    def calc_window_rolls(self, candle: Candle) -> FrozenSet:

        pass  # TODO
