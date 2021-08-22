from typing import Deque, Optional
from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.error_wrappers import ValidationError

from .options import Options
from .timeframe import TimeFrame

class Window(BaseModel):
    """Holds a sequence of timeframes and additional metadata."""

    timeframes: Deque[TimeFrame]

    @validator("timeframes", each_item=True)
    @classmethod
    def insert_timeframe(self, v):
        last = self.timeframes[-1]
        interval_last = last.close_time - last.open_time
        interval_new = v.close_time - v.open_time
        if interval_last != interval_new:
            raise ValidationError(f"Timeframe inserted in {interval_last}ms window instead of {interval_new}ms window.")
        if last.close_time != v.open_time -1:
            raise ValidationError(f"Data leakage: timeframe inserted in {interval_last}ms window is not the next in the sequence.")
        return v


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

    options: Options

    # Data not realtime:
    all_symbols_at_binance: Optional[set]
    selected_symbols: Optional[set]
    # exchange info
    # account info

    # Realtime data:
    symbols: Optional[dict[str, Symbol]]
    # user events
