'''



'''
from typing import Dict

from .options import Interval, Options
from .window import Window


class Pair():


    # Type aliases
    HistCandles  = list[list[str]]
    RawCandle    = dict[str, str]
    ParsedCandle = dict[str, float]


    def __init__(self, symbol: str, options: Options) -> None:
        '''All pairs get initialized in bbot._start_async_client.'''
        
        #TODO: 

        self.symbol  = symbol.upper()
        self.windows = {}
        #TODO: internals with dict. Both dicts-api and attrs-api
        # and use gettr-settrs for attrs. Then no reflection is nescessery

#bot.data.pair['BTCUSDT'].window[Interval.m15]._insert_new_candle(c)
#bot.data.pair['BTCUSDT'].all_windows
# ==
#bot.BTCUSDT.m15._insert_new_candle(c)
#bot.BTCUSDT.all_windows
#bot.all_pairs


#bot.data.pairs getter returnt iterable, zodat:
# for p in bot.pairs:
#   print(p.symbol)
#   for w in p.windows:
#      print(window)
#      for c in w.candles:
#         print(candle)

# @feature
# def my_feature(bot):
#   bot.pairs.


    # Logic related to historical candlestick data -------------------

    def _route_history(self, raw: HistCandles, interval: Interval) -> None:
        '''The complete pipeline for historical candlestick data.'''

        self._verify_history(raw, interval)
        window = self._parse_history(raw, interval)
        setattr(self, interval, window)

    def _verify_history(self, raw: HistCandles, interval: Interval) -> None:
        '''Verifies data integrity of historical candles and throws 
        exceptions when any data leakage/ corruption had been found.'''
        pass


    def _parse_history(self, raw: HistCandles) -> Window:
        '''Convert raw Binance historical data into list of dicts.'''
        pass



    # Logic related to single incoming candles from websocket ---------

    def _route_candle(self, c: RawCandle) -> None:
        '''Complete pipeline for a single incoming candle'''
        pc = self._parse_candle(c)
        wr = self._determine_window_rolls(pc)
        for k, v in wr:
            pass # window.
        
    def _parse_candle(self, c: RawCandle) -> ParsedCandle:
        '''Parses incoming candle from websocket and transforms it
           into more readable dict'''
        pass
        
    def _determine_window_rolls(c: ParsedCandle) -> Dict[Interval, bool]:
        '''An incoming candle can either update the last one in a Window, 
        or be appended as a new candle when it opens. This function
        returns a dict with k=window and v=new'''
        pass