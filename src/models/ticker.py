from pydantic import BaseModel
from datetime import time


class Ticker(BaseModel):
    """Extended 24 hour rolling window statistics.

       {
        "e": "24hrTicker",  // Event type
        "E": 123456789,     // Event time
        "s": "BNBBTC",      // Symbol
        "p": "0.0015",      // Price change
        "P": "250.00",      // Price change percent
        "w": "0.0018",      // Weighted average price
        "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
        "c": "0.0025",      // Last price
        "Q": "10",          // Last quantity
        "b": "0.0024",      // Best bid price
        "B": "10",          // Best bid quantity
        "a": "0.0026",      // Best ask price
        "A": "100",         // Best ask quantity
        "o": "0.0010",      // Open price
        "h": "0.0025",      // High price
        "l": "0.0010",      // Low price
        "v": "10000",       // Total traded base asset volume
        "q": "18",          // Total traded quote asset volume
        "O": 0,             // Statistics open time
        "C": 86400000,      // Statistics close time
        "F": 0,             // First trade ID
        "L": 18150,         // Last trade Id
        "n": 18151          // Total number of trades
    }


    """

    event_time:                    time    # E
    current_price:                 float   # c
    price_24_hours_ago:            float   # o
    high_price_last_24h:           float   # h
    low_price_last_24h:            float   # l
    weighted_avg_price_last_24h:   float   # w
    price_change_last_24h:         float   # p
    price_change_last_24h_percent: float   # P
    base_volume_last_24h:          float   # v
    quote_volume_last_24h:         float   # q
    n_trades_last_24h:             int     # n