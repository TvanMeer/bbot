from ..options import Interval, Options
from .window import Window
from .candle import Candle

class Pair:
    """Holds all windows and additional data related to a single pair,
    like BTCUSDT.
    """

    def __init__(self, symbol, options: Options) -> None:
        self.symbol = symbol
        self.windows = set()
        if Interval.s2 in options.windows.keys:
            self.windows.add(Window(Interval.s2, options.windows[Interval.s2]))


    def _calc_window_rolls():
        pass

    def _insert_and_update():
        pass

