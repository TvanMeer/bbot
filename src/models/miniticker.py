from pydantic import BaseModel


class MiniTicker(BaseModel):
    """24 hour rolling window statistics.

    {
      "e": "24hrMiniTicker",  // Event type
      "E": 123456789,         // Event time
      "s": "BNBBTC",          // Symbol
      "c": "0.0025",          // Close price
      "o": "0.0010",          // Open price
      "h": "0.0025",          // High price
      "l": "0.0010",          // Low price
      "v": "10000",           // Total traded base asset volume
      "q": "18"               // Total traded quote asset volume
    }

    """

    event_time:             int     # E
    current_price:          float   # c
    price_24_hours_ago:     float   # o
    high_price_last_24h:    float   # h
    low_price_last_24h:     float   # l
    base_volume_last_24h:   float   # v
    quote_volume_last_24h:  float   # q
