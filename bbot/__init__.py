"""

Minimal market data fetcher in the making...

"""
import os
import asyncio

from binance import AsyncClient, BinanceSocketManager


class Coin():
    """All realtime data belonging to a symbol, such as BTCUSDT."""

    def __init__(self, symbol, intervals, windowsize):
        self.symbol = symbol
        self.intervals = intervals
        self.windowsize = windowsize
        self.df_names = ['candles_' + iv for iv in intervals]
        [setattr(self, df, []) for df in self.df_names]

        self._historic_frames_downloaded = 0

    def add_historical_candles(self, interval, raw):

        if len(raw) != self.windowsize:
            print(
                f'Error: BinanceAPI returned {len(raw)} candles instead of {self.windowsize} for interval {interval}')

        parsed = []
        for c in raw:
            candle = {
                'open_time':   float(c[0]),
                'open':        float(c[1]),
                'high':        float(c[2]),
                'low':         float(c[3]),
                'close':       float(c[4]),
                'volume':      float(c[5]),
                'close_time':  float(c[6]),
                'qa_volume':   float(c[7]),
                'n_trades':    float(c[8]),
                'tbba_volume': float(c[9]),
                'tbqa_volume': float(c[10])
            }
            parsed.append(candle)

        setattr(self, 'candles_' + interval, parsed)
        self._historic_frames_downloaded += 1

    def add_candle(self, raw):
        if self._historic_frames_downloaded == len(self.intervals):
            pass
        d = raw['data']['k']
        symbol = raw['data']['s']
        closed = d['x']
        candle = {
            'open_time':   float(d['t']),
            'open':        float(d['o']),
            'high':        float(d['h']),
            'low':         float(d['l']),
            'close':       float(d['c']),
            'volume':      float(d['v']),
            'close_time':  float(d['T']),
            'qa_volume':   float(d['q']),
            'n_trades':    float(d['n']),
            'tbba_volume': float(d['V']),
            'tbqa_volume': float(d['Q'])
        }
        print(candle)  # TODO


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
            db.coins[s] = Coin(s, db.intervals, db.windowsize)

        hist = asyncio.create_task(self.download_history(client, db))
        cs = asyncio.create_task(self.start_candle_streams(client, db))
        _ = await asyncio.gather(hist, cs)

    async def download_history(self, client, db):
        for s in db.symbols:
            for iv in db.intervals:
                timestr = self._to_timestring(iv, db.windowsize)
                candles = await client.get_historical_klines(s, iv, timestr)
                db.coins[s].add_historical_candles(iv, candles)

    def _to_timestring(self, interval, windowsize):
        amount = windowsize * int(interval[:-1])
        period = interval[-1]
        if period == 'm':
            return f'{amount} minutes ago UTC'
        elif period == 'h':
            return f'{amount} hours ago UTC'
        elif period == 'd':
            return f'{amount} days ago UTC'
        elif period == 'w':
            return f'{amount} weeks ago UTC'
        elif period == 'M':
            return f'{amount} months ago UTC'
        else:
            raise Exception(f'Error: invalid interval:  {period}')

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
                 windowsize=10
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
