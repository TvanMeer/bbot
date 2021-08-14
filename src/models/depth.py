from typing import Tuple
from datetime import time
from pydantic import BaseModel


class Depth5(BaseModel):
    """Depthchart, showing the best bids and asks in the orderbook.
    Bid1 is the best bid, bid2 the second best.
    Ask1 is the best ask, ask2 the second best etcetera.
    """

    last_update_time: time    
    bid1:  Tuple[float, float]
    ask1:  Tuple[float, float]
    bid2:  Tuple[float, float]
    ask2:  Tuple[float, float]
    bid3:  Tuple[float, float]
    ask3:  Tuple[float, float]
    bid4:  Tuple[float, float]
    ask4:  Tuple[float, float]
    bid5:  Tuple[float, float]
    ask5:  Tuple[float, float]

class Depth10(Depth5):
    bid6:  Tuple[float, float]
    ask6:  Tuple[float, float]
    bid7:  Tuple[float, float]
    ask7:  Tuple[float, float]
    bid8:  Tuple[float, float]
    ask8:  Tuple[float, float]
    bid9:  Tuple[float, float]
    ask9:  Tuple[float, float]
    bid10: Tuple[float, float]
    ask10: Tuple[float, float]

class Depth20(Depth10):
    bid11: Tuple[float, float]
    ask11: Tuple[float, float]
    bid12: Tuple[float, float]
    ask12: Tuple[float, float]
    bid13: Tuple[float, float]
    ask13: Tuple[float, float]
    bid14: Tuple[float, float]
    ask14: Tuple[float, float]
    bid15: Tuple[float, float]
    ask15: Tuple[float, float]
    bid16: Tuple[float, float]
    ask16: Tuple[float, float]
    bid17: Tuple[float, float]
    ask17: Tuple[float, float]
    bid18: Tuple[float, float]
    ask18: Tuple[float, float]
    bid19: Tuple[float, float]
    ask19: Tuple[float, float]
    bid20: Tuple[float, float]
    ask20: Tuple[float, float]