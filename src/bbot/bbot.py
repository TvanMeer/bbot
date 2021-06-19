'''

Main Bot class

'''

from .options import Options
from .client.binance_client import BinanceClient
class Bot():

    # Public
    def stop(self):
        pass

    # Internal
    def __init__(self, options: Options) -> None:
        self._create_client(options)

    def _create_client(self, options: Options) -> None:
        self._bc = BinanceClient(options)
        print('Client is running...')









# Test ------------------------
if __name__ == '__main__':

    options = Options()
    bot = Bot()
