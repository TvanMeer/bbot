from typing import Callable, List, Literal, Optional, Union
from pydantic import BaseModel, validator
from pydantic.types import DirectoryPath, PositiveInt, SecretStr


class Options(BaseModel):
    """Contains all optional arguments for Bbot.
    Required by Bot object at initialization.
    """

    key:              SecretStr                                 = " "
    secret:           SecretStr                                 = " "
    mode:             Literal[
                        "DEBUG", "TEST", "HISTORY", 
                        "STREAM", "PAPER", "TRADE"
                      ]                                         = "TEST"
    datadir:          Optional[DirectoryPath]                   = None
    base_assets:      Union[str, List[str]]                     = ["BTC", "HOT"]
    quote_assets:     Union[str, List[str]]                     = ["USDT"]
    window_intervals: Union[str, List[str]]                     = ["2s", "1m"]
    window_length:    PositiveInt                               = 200
    streams:          Union[str, List[str]]                     = ["candle", "depth5", "miniticker"]
    features:         Optional[Union[Callable, List[Callable]]] = None


    @validator("key", "secret")
    def check_credentials(cls, v):
        assert v == " " or len(v) == 64, "Both key and secret should be of length 64."
        assert v == " " or v.isalnum(), "Both key and secret should be alphanumeric."
        return v


    @validator("base_assets", "quote_assets")
    def check_asset_names(cls, v):
        def check_str(s):
            assert len(s) in range(3, 10), "Asset names should be between 3 and 6 characters long."
            assert s.isalnum(), "Asset names should be alphanumeric, like `BTC` or `USDC`."
        if v is str:
            check_str(v)
            return v.upper()
        else:
            [check_str(s) for s in v]
            return list(map(str.upper, v))


    @validator("window_intervals")
    def check_window_intervals(cls, v):
        def check_str(s):
            assert s.isalnum(), "Window intervals should be alphanumeric, like `1m` or `4h`."
            assert v[-1].lower() in {"s", "m", "h", "d", "w"}, "Window intervals should end with `s`, `m`, `h`, `d` or `w`."
            if v[-1] == "s":
                assert int(v[:-1]) % 2 == 0, "Window second interval should be divisible by 2."
        if v is str:
            check_str(v)
            return v
        else:
            [check_str(s) for s in v]
            return v


    @validator("streams")
    def check_streams(cls, v):
        allowed = {"candle", "miniticker", "ticker", "depth5", "depth10", "depth20"}
        assert set(v).issubset(allowed), f"Valid streams are: {allowed}"
        return v
