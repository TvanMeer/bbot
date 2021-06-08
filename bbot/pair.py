"""

All data and logic related to a pair

"""

class Pair():

    def __init__(self, symbol, options):
        self.symbol = symbol
    
    def add_historical_window(self, interval, raw):
        print('historical window received')

    def add_candle(self, raw):
        print('candle received')