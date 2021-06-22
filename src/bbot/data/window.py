from ..options import Interval
class Window:
    """This class holds only candles of a specific time interval."""

    def __init__(self, 
                 interval: Interval,
                 windowsize: int
                 # data = {} ?
                 #... constructed in client._parse_history
                 ):
        self.iv = interval
        

    def _verify_full_window(self):
        pass
