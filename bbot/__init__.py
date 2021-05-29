"""

Minimal market data fetcher in the making...

"""
import os
import asyncio

from binance import AsyncClient, BinanceSocketManager


class Coin():
    """All realtime data belonging to a symbol, such as BTCUSDT."""

    def __init__(self, symbol):
        pass

    def add_candle(self, raw):
        pass


class DataBase():
    """All realtime data hold in memory. Coin class instances and meta."""

    def __init__(self):
        self.base_assets = None
        self.quote_assets = None
        self.intervals = None
        self.windowsize = None

        self.symbols = set()
        self.coins = {}


class _Api():
    """Interface with Binance through binance-python"""

    def __init__(self, api_key, api_secret, db):
        self.key = api_key
        self.secret = api_secret
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start(db))

    async def start(self, db):
        client = await AsyncClient.create(self.key, self.secret)
        tickers = await client.get_all_tickers()

        for t in tickers:
            for qa in db.quote_assets:
                if t['symbol'].endswith(qa):
                    starts_with = t['symbol'][:-len(qa)]
                    if starts_with in db.base_assets:
                        db.symbols.add(t['symbol'])

        for s in db.symbols:
            db.coins[s] = Coin(s)

        await self.start_candle_streams(client, db)

    async def start_candle_streams(self, client, db):
        bm = BinanceSocketManager(client)
        chanels = [s.lower() + '@kline_1m' for s in db.symbols]
        ms = bm.multiplex_socket(chanels)
        async with ms as mscm:
            while True:
                msg = await mscm.recv()
                symbol = msg['data']['s']
                db.coins[symbol].add_candle(msg)


class BinanceBot():
    """Public API exposed by bbot."""

    def __init__(self, api_key, api_secret,
                 base_assets=['BTC', ],
                 quote_assets=['USDT', ],
                 intervals=['1m', ],
                 windowsize=200
                 ):

        self.data = DataBase()
        self.data.base_assets = [a.upper() for a in base_assets]
        self.data.quote_assets = [q.upper() for q in quote_assets]
        self.data.intervals = intervals
        self.data.windowsize = windowsize

        self._api = _Api(api_key, api_secret, self.data)


if __name__ == '__main__':
    key = os.environ.get('binance_api')
    secret = os.environ.get('binance_secret')
    bot = BinanceBot(key, secret)
