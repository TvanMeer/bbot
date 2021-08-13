from pydantic import BaseModel

class Options(BaseModel):
    """Contains all optional arguments for Bbot.
    Required by Bot object at initialization.
    """

    key              = " "
    secret           = " "
    mode             = "TEST"
    datadir          = "./bbot_data/"
    base_assets      = ["BTC", "HOT"]
    quote_assets     = ["USDT"]
    window_intervals = ["2s", "1m"]
    window_length    = 200
    datasources      = ["candle", "depth20", "ticker"]