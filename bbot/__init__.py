"""

Minimal market data fetcher in the making...

"""
import os
import asyncio
import json

from binance import AsyncClient


class Coin():
    """All realtime data belonging to a symbol, such as BTCUSDT."""

    def __init__(self, symbol):
        pass


class DataBase():
    """All realtime data hold in memory. Coin class instances and meta."""

    def __init__(self):
        self.base_assets = None
        self.quote_assets = None
        self.intervals = None
        self.windowsize = None


class _Api():
    """Interface with Binance through binance-python"""

    def __init__(self, api_key, api_secret, db):
        self.key = api_key
        self.secret = api_secret
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start(db))

    async def start(self, db):
        client = await AsyncClient.create(self.key, self.secret)
        res = await client.get_exchange_info()
        print(json.dumps(res, indent=2))
        await client.close_connection()


class BinanceBot():
    """Public API exposed by bbot."""

    def __init__(self, api_key, api_secret,
                 base_assets=["BTC", ],
                 quote_assets=["USDT", ],
                 intervals=["1m", ],
                 windowsize=200
                 ):

        self.data = DataBase()
        self.data.base_assets = base_assets
        self.data.quote_assets = quote_assets
        self.data.intervals = intervals
        self.data.windowsize = windowsize

        self._api = _Api(api_key, api_secret, self.data)


if __name__ == "__main__":
    key = os.environ.get("binance_api")
    secret = os.environ.get("binance_secret")
    bot = BinanceBot(key, secret)
