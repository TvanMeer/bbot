from typing import Callable, Iterable, Optional, Union
from collections.abc import Iterable as CollectionsIter
from enum import Enum

from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError
from pydantic.types import DirectoryPath, PositiveInt, SecretStr


class Options(BaseModel):
    """Contains all optional arguments for Bbot.
    Required by Bot object at initialization.
    """

    class Mode(str, Enum):
        test       = "test"
        history    = "history"
        stream     = "stream"
        paper      = "paper"
        trade      = "trade"

    class Stream(str, Enum):
        candle     = "candle"
        miniticker = "miniticker"
        ticker     = "ticker"
        depth5     = "depth5"
        depth10    = "depth10"
        depth20    = "depth20"
        orderbook  = "orderbook"
        aggtrade   = "aggtrade"
        trade      = "trade"

    class Interval(str, Enum):
        second_2   = "2s"
        minute_1   = "1m"
        minute_3   = "3m"
        minute_5   = "5m"
        minute_15  = "15m"
        minute_30  = "30m"
        hour_1     = "1h"
        hour_2     = "2h"
        hour_4     = "4h"
        hour_6     = "6h"
        hour_8     = "8h"
        hour_12    = "12h"
        day_1      = "1d"
        day_3      = "3d"
        week_1     = "1w"



    key:              SecretStr                                     = " "
    secret:           SecretStr                                     = " "
    mode:             Mode                                          = Mode.test
    datadir:          Optional[DirectoryPath]                       = None
    base_assets:      Union[str, Iterable[str]]                     = ["BTC", "HOT"]
    quote_assets:     Union[str, Iterable[str]]                     = ["USDT"]
    window_intervals: Union[Interval, Iterable[Interval]]           = [Interval.second_2, Interval.minute_1]
    window_length:    PositiveInt                                   = 200
    streams:          Optional[Union[Stream, Iterable[Stream]]]     = [Stream.candle, Stream.depth5, Stream.miniticker]
    features:         Optional[Union[Callable, Iterable[Callable]]] = None



    @validator("key", "secret")
    @classmethod
    def _check_credentials(cls, v):
        if not v == " " or not len(v) == 64:
            raise ValidationError("Both key and secret should be of length 64.")
        if not v == " " or not v.islanum():
            raise ValidationError("Both key and secret should be alphanumeric.")
        return v


    @validator("base_assets", "quote_assets")
    @classmethod
    def _check_asset_names(cls, v):
        def check_str(s):
            if not len(s) in range(3, 6):
                raise ValidationError("Asset names should be between 3 and 6 characters long.")
            if not s.isalnum():
                raise ValidationError("Asset names should be alphanumeric, like `BTC` or `USDC`.")

        asset_names = v.lower() if v is type(str) else list(map(str.lower, v))
        map(check_str, asset_names)
        return list(asset_names)


    @validator("streams")
    @classmethod
    def _make_stream_iterable(cls, v):
        if not isinstance(v, CollectionsIter):
            return [v]
        return v
