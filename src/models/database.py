from typing import Deque, Optional
from datetime import time
from pydantic import BaseModel

from candle import Candle
from ticker import MiniTicker, Ticker
from depth import Depth5, Depth10, Depth20


class TimeFrame(BaseModel):
    """Holds all data related to market events between two points in time.
    A window is a sequence of timeframes. If only candle data is
    selected, then `timeframe` is equivalent to `candle`.
    Depth is the depthchart at open time of this timeframe.
    """

    open_time:  time
    close_time: time
    candle:     Optional[Candle]
    miniticker: Optional[MiniTicker]
    ticker:     Optional[Ticker]
    depth5:     Optional[Depth5]
    depth10:    Optional[Depth10]
    depth20:    Optional[Depth20]


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    timeframes: Deque[TimeFrame]


class Symbol(BaseModel):
    """Holds all data related to a symbol, such as `BTCUSDT`"""

    windows: dict[str, Window]


class DataBase(BaseModel):
    """Contains all data.
    This class is injected in user defined feature functions.

    db -> symbol -> window -> deque[timeframes]

    Database contains one or more symbols, like `BTCUSDC` and `ETHBTC`.
    A symbol contains one or more windows, like `1m` and `4h`.
    A window holds a sequence of timeframes.
    """

    symbols: dict[str, Symbol]

