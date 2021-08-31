from collections import deque
from typing import Deque, Optional, TypeVar, Union
from datetime import datetime, timedelta

from pydantic import BaseModel

from .candle import Candle
from .ticker import MiniTicker, Ticker
from .depth import Depth5, Depth10, Depth20
from .orderbook import OrderBookUpdate
from .trade import AggTrade, Trade

_TimeFrame = TypeVar("_TimeFrame", bound="TimeFrame")

class TimeFrame(BaseModel):
    """Contains all data related to market events between two points in time.

    Candle covers this timeframe and is updated until this timeframe is closed.
    The other fields are updated until this timeframe is closed.
    """

    open_time:          datetime
    close_time:         datetime

    candle:             Optional[Candle]                          = None
    miniticker:         Optional[MiniTicker]                      = None
    ticker:             Optional[Ticker]                          = None
    depth:              Optional[Union[Depth5, Depth10, Depth20]] = None
    orderbook_updates:  Deque[OrderBookUpdate]                    = deque()
    aggtrades:          Deque[AggTrade]                           = deque()
    trades:             Deque[Trade]                              = deque()



    @staticmethod
    def create_next_timeframe(previous_open_time: datetime, previous_close_time: datetime) -> _TimeFrame:
        """Creates the next timeframe for a window."""

        delta = previous_close_time - previous_open_time
        milli = timedelta(milliseconds=1)
        return TimeFrame(
            open_time  = previous_close_time + milli,
            close_time = previous_close_time + milli + delta
        )
