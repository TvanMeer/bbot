from collections import deque
from datetime import timedelta
from typing import Deque, Optional

from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError

from .candle import Candle
from .options import Options
from .timeframe import TimeFrame


class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    interval:                   Options.Interval
    timeframes:                 Deque[TimeFrame]    = deque()

    _last_candle_update:        Optional[Candle]    = None
    _last_candle_update_closed: Optional[bool]      = None
    _latency:                   Optional[timedelta] = None

    

    @validator("timeframes", each_item=True)
    @classmethod
    def check_timeframe_time(self, v):
        last_frame = self.timeframes[-1]
        delta_last_frame = last_frame.close_time - last_frame.open_time
        delta_new_frame = v.close_time - v.open_time
        if delta_new_frame != delta_last_frame:
            raise ValidationError("Timeframe inserted in the wrong window.")
        if last_frame.close_time != v.open_time -1:
            raise ValidationError(f"Data leakage: timeframe inserted in {self.interval.value} window is not the next in the sequence.")
        return v