from .options import Options
from .client.binance_client import BinanceClient

class Bot():
    """Main class that holds public API."""

    

    # Internal
    def __init__(self, options: Options) -> None:
        self._create_client(options)

    def _create_client(self, options: Options) -> None:
        self._bc = BinanceClient(options)
        print('Client is running...')

    # Public
    def stop(self):
        pass









# Test ------------------------
if __name__ == '__main__':

    options = Options()
    bot = Bot()
