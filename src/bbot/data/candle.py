from typing import Optional
from datetime import datetime

class Candle:
    """A single candle."""

    def __init__(self, 
                 event_time:                   Optional(datetime),
                 symbol:                       str,
                 open_time:                    datetime, 
                 close_time:                   datetime,
                 is_closed:                    bool,
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

        self._event_time                   = event_time
        self._symbol                       = symbol
        self._open_time                    = open_time
        self._close_time                   = close_time
        self._is_closed                    = is_closed
        self._open_price                   = open_price
        self._close_price                  = close_price
        self._high_price                   = high_price
        self._low_price                    = low_price
        self._base_asset_volume            = base_asset_volume
        self._n_trades                     = n_trades
        self._quote_asset_volume           = quote_asset_volume
        self._taker_buy_base_asset_volume  = taker_buy_base_asset_volume
        self._taker_buy_quote_asset_volume = taker_buy_quote_asset_volume

        self._missing                      = False


    # Attribute names

    @property
    def event_time(self) -> datetime:
        return self._event_time

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def open_time(self) -> datetime:
        return self._open_time

    @property
    def close_time(self) -> datetime:
        return self._close_time

    @property
    def is_closed(self) -> bool:
        return self._is_closed

    @property
    def open_price(self) -> float:
        return self._open_price

    @property
    def close_price(self) -> float:
        return self._close_price

    @property
    def high_price(self) -> float:
        return self._high_price

    @property
    def low_price(self) -> float:
        return self._low_price

    @property
    def base_asset_volume(self) -> float:
        return self._base_asset_volume

    @property
    def n_trades(self) -> int:
        return self._n_trades

    @property
    def quote_asset_volume(self) -> float:
        return self._quote_asset_volume

    @property
    def taker_buy_base_asset_volume(self) -> float:
        return self._taker_buy_base_asset_volume

    @property
    def taker_buy_quote_asset_volume(self) -> float:
        return self._taker_buy_quote_asset_volume
        

    @property
    def missing(self) -> bool:
        return self._missing

    @missing.setter
    def missing(self, missing_flag: bool) -> None:
        self._missing = missing_flag



    # Shorthand attribute names

    @property
    def et(self) -> datetime:
        return self._event_time

    @property
    def sym(self) -> str:
        return self._symbol

    @property
    def ot(self) -> datetime:
        return self._open_time

    @property
    def ct(self) -> datetime:
        return self._close_time

    @property
    def o(self) -> float:
        return self._open_price

    @property
    def c(self) -> float:
        return self._close_price

    @property
    def h(self) -> float:
        return self._high_price

    @property
    def l(self) -> float:
        return self._low_price

    @property
    def bav(self) -> float:
        return self._base_asset_volume

    @property
    def n(self) -> int:
        return self._n_trades

    @property
    def qav(self) -> float:
        return self._quote_asset_volume

    @property
    def tbbav(self) -> float:
        return self._taker_buy_base_asset_volume

    @property
    def tbqav(self) -> float:
        return self._taker_buy_quote_asset_volume
