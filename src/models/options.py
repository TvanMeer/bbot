from typing import Callable, List, Literal, Optional, Union
from pydantic import BaseModel
from pydantic.types import DirectoryPath, SecretStr


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
    window_length:    int                                       = 200
    datasources:      Union[str, List[str]]                     = ["candle", "depth5", "miniticker"]
    features:         Optional[Union[Callable, List[Callable]]] = None
