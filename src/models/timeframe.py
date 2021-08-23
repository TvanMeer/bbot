from typing import Deque, Optional, Union
from datetime import time

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError

from .candle import Candle
from .ticker import MiniTicker, Ticker
from .depth import Depth5, Depth10, Depth20
from .orderbook import OrderBook
from .trade import AggTrade, Trade


class TimeFrame(BaseModel):
    """Holds all data related to market events between two points in time.
    A window is a sequence of timeframes. If only candle data is
    selected, then `timeframe` is equivalent to `candle`.
    Depth is the depthchart at close time of this timeframe.
    """

    _candle_prev_2s:     Candle

    open_time:           time
    close_time:          time

    candle:              Optional[Candle]
    miniticker:          Optional[MiniTicker]
    ticker:              Optional[Ticker]
    depth:               Optional[Union[Depth5, Depth10, Depth20]]
    orderbook:           Optional[OrderBook]
    aggtrade:            Optional[Deque[AggTrade]]
    trade:               Optional[Deque[Trade]]



    @validator("close_time")
    @classmethod
    def check_interval(self, v):
        s = 1000
        m = s * 60
        h = m * 60
        d = h * 24
        w = d * 7
        if v.close_time - self.open_time in {
            s * 2,
            m,
            m * 3,
            m * 5,
            m * 15,
            m * 30,
            h,
            h * 2,
            h * 4,
            h * 6,
            h * 8,
            h * 12,
            d,
            d * 3,
            w,
        }:
            return v
        else:
            raise ValidationError("Open or close time is invalid.")



    @validator("candle")
    @classmethod
    def update_candle(self, v):
        # New candle
        if self.candle == None:
            self._candle_prev_2s = v
            return v

        if v.open_time < self.open_time:
            raise ValidationError(
                "Attempted to add candle to the wrong timeframe. Needs to be in a previous timeframe."
            )
        if v.close_time > self.close_time:
            raise ValidationError(
                "Attempted to add candle to the wrong timeframe. Needs to be in the next timeframe."
            )

        # Update candle
        new = self.candle
        new.close_price = v.close_price
        new.high_price = v.high_price if v.high_price > new.high_price else new.high_price
        new.low_price = v.low_price if v.low_price < new.low_price else new.low_price

        is_new_1m = (
            v.open_time != self._candle_prev_2s.open_time
            and v.closetime != self._candle_prev_2s.close_time
        )
        if is_new_1m:
            new.base_volume += v.base_volume
            new.quote_volume += v.quote_volume
            new.base_volume_taker += v.base_volume_taker
            new.quote_volume_taker += v.quote_volume_taker
            new.n_trades += v.n_trades
        else:
            new.base_volume += v.base_volume - self._candle_prev_2s.base_volume
            new.quote_volume += v.quote_volume - self._candle_prev_2s.quote_volume
            new.base_volume_taker += v.base_volume_taker - self._candle_prev_2s.base_volume_taker
            new.quote_volume_taker += v.quote_volume_taker - self._candle_prev_2s.quote_volume_taker
            new.n_trades += v.n_trades - self._candle_prev_2s.n_trades

        self._candle_prev_2s = v
        return new



    @validator("miniticker", "ticker")
    @classmethod
    def update_miniticker(self, v):
        if v.event_time < self.open_time or v.event_time > self.close_time:
            raise ValidationError(
                f"Attempted to add miniticker in the wrong timeframe. Open en close time are {self.open_time} and {self.close_time}, but the event_time of new value is {v.event_time}."
            )
        return v
