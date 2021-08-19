from typing import Deque

from pydantic import BaseModel
from pydantic.types import condecimal


class Bid(BaseModel):
    price: condecimal(decimal_places=8, gt=0)
    quantity: condecimal(decimal_places=8, gt=0)


class Ask(BaseModel):
    price: condecimal(decimal_places=8, gt=0)
    quantity: condecimal(decimal_places=8, gt=0)


class OrderBook(BaseModel):
    """Orderbook within timeframe.

    {
      "lastUpdateId": 1027024,
      "bids": [
        [
          "4.00000000",     // PRICE
          "431.00000000"    // QTY
        ]
      ],
      "asks": [
        [
          "4.00000200",
          "12.00000000"
        ]
      ]
    }

    """

    bids: Deque[Bid]
    asks: Deque[Ask]
