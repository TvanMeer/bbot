from typing import Optional
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