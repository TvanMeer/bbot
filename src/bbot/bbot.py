from .options import Options
from .client.binance_client import _BinanceClient


class Bot:
    """Main class that holds public API."""

    # Public
    def stop(self):
        pass

    # Internal
    def __init__(self, options: Options) -> None:
        self._create_client(options)

    def _create_client(self, options: Options) -> None:
        self._bc = _BinanceClient(options)
        print("Client is running...")
