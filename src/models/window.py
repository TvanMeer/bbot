# pylint: disable=no-name-in-module

from collections import deque
from datetime import timedelta
from typing import Deque, Optional

from pydantic import BaseModel

from .candle import Candle
from .options import Options
from .timeframe import TimeFrame


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    interval:                   Options.Interval
    timeframes:                 Deque[TimeFrame]    = deque()

    _last_candle_update:        Optional[Candle]    = None
    _last_candle_update_closed: Optional[bool]      = None
    _history_downloaded:        bool                = False
    _latency:                   Optional[timedelta] = None
