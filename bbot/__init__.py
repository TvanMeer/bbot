"""

Minimal market data fetcher in the making...

"""
import os

options = {}


class Coin():
    """All realtime data belonging to a symbol, such as BTCUSDT."""

    def __init__(self, symbol):
        pass


class DataBase():
    """All realtime data hold in memory. Coin class instances and meta."""

    def __init__(self, options):
        pass


class Api():
    """Interface with Binance through binance-python"""

    def __init__(self, api_key, api_secret):
        self.key = api_key
        self.secret = api_secret


class BinanceBot():
    """Public API exposed by bbot."""

    def __init__(self, api_key, api_secret, options):
        self.api = Api(api_key, api_secret)


if __name__ == "__main__":
    key = os.environ.get("binance_api")
    secret = os.environ.get("binance_secret")
    bot = BinanceBot(key, secret)
