'''

Main Bot class

'''

from . import options
from client import binance_client
class Bot():

    # Public
    def stop(self):
        pass

    # Internal
    def __init__(self) -> None:
        self._create_client()

    def _create_client(self) -> None:
        self.bc = binance_client.BinanceClient()
        print('client initialized...')









# Test ------------------------
if __name__ == '__main__':

    options = options.Options()
    bot = Bot()
