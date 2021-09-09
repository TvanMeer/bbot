# pylint: disable=no-name-in-module

from typing import Callable, Optional
from collections.abc import Iterable

from pydantic import BaseModel, validator
from pydantic.error_wrappers import ValidationError
from pydantic.types import DirectoryPath, SecretStr

from ..bbot.constants import Mode, Interval, Stream

class Options(BaseModel):
    """Contains all optional arguments for Bbot.
    Required by Bot object at initialization.
    """

    key:              SecretStr               = " "
    secret:           SecretStr               = " "
    mode:             Mode                    = Mode.TEST
    datadir:          Optional[DirectoryPath] = None
    base_assets:      set[str]                = {"BTC", "HOT"}
    quote_assets:     set[str]                = {"USDT"}
    window_intervals: set[Interval]           = {Interval.SECOND_2, Interval.MINUTE_1}
    window_length:    int                     = 200
    streams:          Optional[set[Stream]]   = {Stream.CANDLE, Stream.DEPTH5, Stream.MINITICKER}
    features:         Optional[set[Callable]] = None



    @validator("key", "secret")
    @classmethod
    def _check_credentials(cls, v):
        if not v == " " and not len(v) == 64:
            raise ValidationError("Both key and secret should be of length 64.")
        if not v == " " and not v.islanum():
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

        if isinstance(v, str):
            check_str(v)
            return {v.lower()}
        elif isinstance(v, Iterable):
            map(check_str, v)
            lower = set(map(str.lower, v))
            return lower
        else:
            raise ValidationError("Asset names should be strings.")


    @validator("window_intervals")
    @classmethod
    def _make_window_intervals(cls, v):

        def iv(val):
            val = val.lower()
            if val in list(map(str, cls.Interval)):
                return cls.Interval(val)
            else:
                raise ValidationError("Invalid window intervals.")

        if isinstance(v, str):
            return {iv(v)}
        elif isinstance(v, Iterable):
            itvs = set()
            [itvs.add(iv(s)) for s in v]
            return itvs
        else:
            raise ValidationError("Invalid window intervals: should be strings.")
        

    @validator("window_length")
    @classmethod
    def _check_window_length(cls, v):
        if v == "*":
            return 0
        elif isinstance(v, int) and v >= 0:
            return v
        else:
            raise ValidationError("Invalid window length.")


    @validator("streams")
    @classmethod
    def _make_streams(cls, v):

        def stream(val):
            val = val.lower()
            if val in list(map(str, cls.Stream)):
                return cls.Stream(val)
            else:
                raise ValidationError("Invalid streams.")

        if isinstance(v, str):
            return {stream(v)}
        elif isinstance(v, Iterable):
            strms = set()
            [strms.add(stream(s)) for s in v]
            return strms
        else:
            raise ValidationError("Invalid streams: should be strings.")
   
