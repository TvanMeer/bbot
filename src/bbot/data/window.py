from ..options import Interval
from .candle import Candle
class Window:
    """This class holds only candles of a specific time interval."""

    def __init__(self, 
                 interval: Interval,
                 windowsize: int
                 # data = {} ?
                 ):
        self.iv = interval
        

    def _add_historical_candle(self, candle: Candle):
        """Verifies and adds a single historical candle passed by
        client._parse_historical_candle().
        """

        pass #TODO
