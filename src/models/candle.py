from datetime import time

from pydantic import BaseModel
from pydantic.types import PositiveInt, condecimal


class Candle(BaseModel):
    """Candlestick from websocket stream.

    {
      "e": "kline",     // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "k": {
        "t": 123400000, // Kline start time
        "T": 123460000, // Kline close time
        "s": "BNBBTC",  // Symbol
        "i": "1m",      // Interval
        "f": 100,       // First trade ID
        "L": 200,       // Last trade ID
        "o": "0.0010",  // Open price
        "c": "0.0020",  // Close price
        "h": "0.0025",  // High price
        "l": "0.0015",  // Low price
        "v": "1000",    // Base asset volume
        "n": 100,       // Number of trades
        "x": false,     // Is this kline closed?
        "q": "1.0000",  // Quote asset volume
        "V": "500",     // Taker buy base asset volume
        "Q": "0.500",   // Taker buy quote asset volume
        "B": "123456"   // Ignore
      }
    }

    """

    open_price:         condecimal(decimal_places=8, gt=0)   # o
    close_price:        condecimal(decimal_places=8, gt=0)   # c
    high_price:         condecimal(decimal_places=8, gt=0)   # h
    low_price:          condecimal(decimal_places=8, gt=0)   # l
    base_volume:        condecimal(decimal_places=8)         # v
    quote_volume:       condecimal(decimal_places=8)         # q
    base_volume_taker:  condecimal(decimal_places=8)         # V
    quote_volume_taker: condecimal(decimal_places=8)         # Q
    n_trades:           PositiveInt                          # n
