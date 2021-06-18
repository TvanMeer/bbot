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
    def __init__(self, options: options.Options) -> None:
        self._create_client(options)

    def _create_client(self, options: options.Options) -> None:
        self.bc = binance_client.BinanceClient(options)
        print('Client is running...')









# Test ------------------------
if __name__ == '__main__':

    options = options.Options()
    bot = Bot()
