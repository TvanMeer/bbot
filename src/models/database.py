from typing import Deque, Optional, Union
from datetime import time
from pydantic import BaseModel

from .options import Options
from .candle import Candle
from .ticker import MiniTicker, Ticker
from .depth import Depth5, Depth10, Depth20


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
    depth:      Optional[Union[Depth5, Depth10, Depth20]]


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    timeframes: Deque[TimeFrame]


class Symbol(BaseModel):
    """Holds all data related to a symbol, such as `BTCUSDT`,
    and additional metadata.
    """

    windows: dict[Options.Interval, Window]


class DataBase(BaseModel):
    """Contains all data.
    This class is injected in user defined feature functions.

    db -> dict[symbols] -> dict[windows] -> deque[timeframes]

    Database contains one or more symbols, like `BTCUSDC` and `ETHBTC`.
    A symbol contains one or more windows, like `1m` and `4h`.
    A window holds a sequence of timeframes.

    Example:
    Get last 1 minute candle for symbol `BTCUSDC`:

    db.symbols["BTCUSDC"].windows[Interval.minute_1].timeframes[-1]
    """

    options:                Options

    # Data not realtime:
    all_symbols_at_binance: Optional[set]
    selected_symbols:       Optional[set]
    # exchange info
    # account info

    # Realtime data:
    symbols:                Optional[dict[str, Symbol]]
    # user events

