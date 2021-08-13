from pydantic import BaseModel
from datetime import time


class Depth5(BaseModel):
    """Depthchart, showing the best bids and asks in the orderbook.
    Bid1 is the best bid, bid2 the second best.
    Ask1 is the best ask, ask2 the second best etcetera.
    """

    last_update_time: time    
    bid1:  float
    ask1:  float
    bid2:  float
    ask2:  float
    bid3:  float
    ask3:  float
    bid4:  float
    ask4:  float
    bid5:  float
    ask5:  float

class Depth10(Depth5):
    bid6:  float
    ask6:  float
    bid7:  float
    ask7:  float
    bid8:  float
    ask8:  float
    bid9:  float
    ask9:  float
    bid10: float
    ask10: float

class Depth20(Depth10):
    bid11: float
    ask11: float
    bid12: float
    ask12: float
    bid13: float
    ask13: float
    bid14: float
    ask14: float
    bid15: float
    ask15: float
    bid16: float
    ask16: float
    bid17: float
    ask17: float
    bid18: float
    ask18: float
    bid19: float
    ask19: float
    bid20: float
    ask20: float