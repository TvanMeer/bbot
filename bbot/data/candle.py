'''

A single candle.

'''
from datetime import datetime

class Candle:

    def __init__(self, 
                 event_time:                   datetime,
                 symbol:                       str,
                 open_time:                    datetime, 
                 close_time:                   datetime,
                 open_price:                   float, 
                 close_price:                  float,
                 high_price:                   float, 
                 low_price:                    float,
                 base_asset_volume:            float,
                 n_trades:                     int,
                 quote_asset_volume:           float,
                 taker_buy_base_asset_volume:  float,
                 taker_buy_quote_asset_volume: float
                 ) -> None:

        self.event_time                   = event_time
        self.symbol                       = symbol
        self.open_time                    = open_time
        self.close_time                   = close_time
        self.open_price                   = open_price
        self.close_price                  = close_price
        self.high_price                   = high_price
        self.low_price                    = low_price
        self.base_asset_volume            = base_asset_volume
        self.n_trades                     = n_trades
        self.quote_asset_volume           = quote_asset_volume
        self.taker_buy_base_asset_volume  = taker_buy_base_asset_volume
        self.taker_buy_quote_asset_volume = taker_buy_quote_asset_volume
        self.missing                      = False

    
    # Shorthand attribute names
    @property
    def et(self):
        return self.event_time

    @property
    def sym(self):
        return self.symbol

    @property
    def ot(self):
        return self.open_time

    @property
    def ct(self):
        return self.close_time

    @property
    def o(self):
        return self.open_price

    @property
    def c(self):
        return self.close_price

    @property
    def h(self):
        return self.high_price

    @property
    def l(self):
        return self.low_price

    @property
    def bav(self):
        return self.base_asset_volume

    @property
    def n(self):
        return self.n_trades

    @property
    def qav(self):
        return self.quote_asset_volume

    @property
    def tbbav(self):
        return self.taker_buy_base_asset_volume

    @property
    def tbqav(self):
        return self.taker_buy_quote_asset_volume

    @property
    def m(self):
        return self.missing
