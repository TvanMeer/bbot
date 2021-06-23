from typing import Any, Dict, FrozenSet, List
from binance import AsyncClient, BinanceSocketManager
import asyncio
import datetime

from .base_client      import BaseClient
from ..options         import Interval, Options
from ..data.database   import Database
from ..data.candle     import Candle
from ..data.user_event import UserEvent


class BinanceClient(BaseClient):
    """Binance client implementation"""

    
    def __init__(self, options: Options):
        """Starts bootstrapping logic in parents constructor."""

        super().__init__(options)
        self._shutdown_flag = False


    def _shutdown(self):
        """Shutdown client."""
        self._shutdown_flag = True
        # process.join()


    async def _create_async_client(options: Options) -> AsyncClient:
        """Returns a python-binance.AsyncClient object."""

        client = await AsyncClient.create(api_key    = options.api_key, 
                                          api_secret = options.api_secret)
        return client

    async def _download_all_symbols(client: AsyncClient) -> List[Dict]:
        """Downloads ticker data that contains all symbols of trading pairs
        on Binance. This is a list of dicts with k=symbol and v=close_price.
        """

        raw = await client.get_all_tickers()
        return raw


    def _parse_all_symbols(raw: List[Dict]) -> FrozenSet[str]:
        """Filters and returns all symbols of pairs being traded
        at Binance from raw data and returns them as a set.
        """

        all_symbols = set()
        [all_symbols.add(t['symbol']) for t in raw]
        return frozenset(all_symbols)


    async def _download_history(self, symbols: FrozenSet[str], client: AsyncClient, db: Database) -> None:
        """Downloads all windows of historical candlestick data, 
        as raw data in the format provided by the API. Then iterates through
        each window and passes a single candle to _parse_historical_candle().
        """

        for s in symbols:
            for w in self.options.windows.keys():
                if w == Interval.s2:
                    continue
                timestr = self._to_timestring(w.name, w.value)
                candles = await client.get_historical_klines(s, w.name, timestr)
                for c in candles:
                    self._parse_historical_candle(c, s, Interval[w], db)
                asyncio.sleep(1)


    def _to_timestring(interval: Interval, windowsize: int) -> str:
        # Helperfunction to download history with binance-python.

        amount = int(interval.name[1:]) * windowsize
        time_frame = interval.name[0]
        if time_frame == 'm':
            return f'{amount} minutes ago UTC'
        elif time_frame == 'h':
            return f'{amount} hours ago UTC'
        elif time_frame == 'd':
            return f'{amount} days ago UTC'
        elif time_frame == 'w':
            return f'{amount} weeks ago UTC'
        else:
            raise Exception(f'Error: invalid interval:  {time_frame}')


    def _parse_historical_candle(self, raw: List, symbol: str, interval: Interval, db: Database) -> None:
        """Takes single candle from raw historical candlestick data coming 
        from _download_history() and transforms it to a Candle object.
        Then passes this candle object to the corresponding Window instance in 
        db.<Pair>.<Window>._add_historical_candle().
        """

        hc = Candle(event_time                   = None,
                    symbol                       = symbol,
                    open_time                    = self._ms_to_datetime(int(raw[0])),
                    close_time                   = self._ms_to_datetime(int(raw[6])),
                    is_closed                    = True,
                    open_price                   = float(raw[1]),
                    close_price                  = float(raw[4]),
                    high_price                   = float(raw[2]),
                    low_price                    = float(raw[3]),
                    base_asset_volume            = float(raw[5]),
                    n_trades                     = int(raw[8]),
                    quote_asset_volume           = float(raw[7]),
                    taker_buy_base_asset_volume  = float(raw[9]),
                    taker_buy_quote_asset_volume = float(raw[10])
                    )

        db.pairs[symbol].windows[symbol]._add_historical_candle(hc)
        

    def _ms_to_datetime(ms: int) -> datetime:
        # Helperfunction that creates datetime object.

        return datetime.datetime.fromtimestamp(ms / 1000.0, tz=datetime.timezone.utc)


    async def _start_candle_sockets(self, symbols: FrozenSet[str], client: AsyncClient, db: Database) -> None:
        """Starts one or multiple websockets that stream candlestick data.
        Each socket streams data related to one pair. Only time interval 
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes parsed candle to db.<Pair>._calc_window_rolls().
        """

        bm      = BinanceSocketManager(client)
        chanels = [s.lower() + '@kline_1m' for s in symbols]
        ms      = bm.multiplex_socket(chanels)
        async with ms as stream:
            while self._shutdown_flag == False:
                msg    = await stream.recv()
                symbol = msg['data']['s']
                parsed = self._parse_candle(msg)
                db.pairs[symbol]._calc_window_rolls(parsed)


    def _parse_candle(self, raw: Dict) -> Candle:
        """Takes raw candle data from a single candle and returns a Candle object."""
        
        d = raw['data']['k']
        return Candle(event_time                   = self._ms_to_datetime(int(raw['data']['E'])),
                      symbol                       =                          raw['data']['s'],
                      open_time                    =           self._ms_to_datetime(int(d['t'])),
                      close_time                   =           self._ms_to_datetime(int(d['T'])),
                      is_closed                    =                               bool(d['x']),
                      open_price                   =                              float(d['o']),
                      close_price                  =                              float(d['c']),
                      high_price                   =                              float(d['h']),
                      low_price                    =                              float(d['l']),
                      base_asset_volume            =                              float(d['v']),
                      n_trades                     =                                int(d['n']),
                      quote_asset_volume           =                              float(d['q']),
                      taker_buy_base_asset_volume  =                              float(d['V']),
                      taker_buy_quote_asset_volume =                              float(d['Q'])
                      )


    async def _start_user_socket(client: AsyncClient) -> None:
        """Starts a websocket that listens to user events."""
        
        pass #TODO

    def _parse_user_event(event: Any) -> UserEvent:
        
        """Parses a message from a user socket. This message is one of
        the following events:
        1) Account update
        2) Order update
        3) Trade update
        """

        pass #TODO