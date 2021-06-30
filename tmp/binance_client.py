from typing import Any, Dict, FrozenSet, List
from binance import AsyncClient, BinanceSocketManager
import asyncio
import datetime

from .base_client import _BaseClient
from ..options import Options
from ..data.user_event import UserEvent


class _BinanceClient(_BaseClient):
    """Binance client implementation

    Usage:
    client = _BinanceClient(options)
    client.start()
    client.start_loops()
    """

    def __init__(self, options: Options):
        super().__init__(options)

    async def create_async_client(self, options: Options) -> AsyncClient:
        """Returns a python-binance.AsyncClient object."""

        return await AsyncClient.create(
            api_key=options.api_key, api_secret=options.api_secret
        )

    async def download_all_symbols(self, client: AsyncClient) -> List[Dict]:
        """Downloads ticker data that contains all symbols of trading pairs
        on Binance. This is a list of dicts with k=symbol and v=close_price.
        """

        return await client.get_all_tickers()

    def parse_all_symbols(self, payload: List[Dict]) -> FrozenSet[str]:
        """Gets all symbols of pairs that are traded at Binance from ticker data.
        Returns set of all symbols.
        """

        all_symbols = set()
        [all_symbols.add(t["symbol"]) for t in payload]
        return frozenset(all_symbols)

    async def download_history(
        self, symbols: FrozenSet[str], client: AsyncClient, db: _Data
    ) -> None:
        """Downloads all windows of historical candlestick data,
        as raw data in the format provided by the API. Then iterates through
        each window and passes candles one by one to self.parse_historical_candle().
        """

        for s in symbols:
            for iv, size in self.options.windows.keys():
                if iv == "2s":
                    continue
                timestr = self.to_timestring(iv, size)
                candles = await client.get_historical_klines(s, iv, timestr)
                for c in candles:
                    await self.q.put((s, iv, c))

                await asyncio.sleep(1)

    def to_timestring(self, interval: str, windowsize: int) -> str:
        # Helperfunction to download history with binance-python.

        amount = int(interval[:-1]) * windowsize
        time_frame = interval[-1]
        if time_frame == "m":
            return f"{amount} minutes ago UTC"
        elif time_frame == "h":
            return f"{amount} hours ago UTC"
        elif time_frame == "d":
            return f"{amount} days ago UTC"
        elif time_frame == "w":
            return f"{amount} weeks ago UTC"
        else:
            raise Exception(f"Error: invalid interval:  {time_frame}")

    def parse_historical_candle(
        self, raw: List, symbol: str, interval: str, db: _Database
    ) -> Candle:
        """Takes single candle from raw historical candlestick data coming
        from self.download_history() and transforms it to a Candle object.
        Then passes this candle object to the corresponding Window instance in
        db.<Pair>.<Window>._add_historical_candle(). #TODO docs aanpassen
        """

        return Candle(
            event_time=None,
            symbol=symbol,
            open_time=self.ms_to_datetime(int(raw[0])),
            close_time=self.ms_to_datetime(int(raw[6])),
            is_closed=True,
            open_price=float(raw[1]),
            close_price=float(raw[4]),
            high_price=float(raw[2]),
            low_price=float(raw[3]),
            base_asset_volume=float(raw[5]),
            n_trades=int(raw[8]),
            quote_asset_volume=float(raw[7]),
            taker_buy_base_asset_volume=float(raw[9]),
            taker_buy_quote_asset_volume=float(raw[10]),
        )

    def ms_to_datetime(self, ms: int) -> datetime:
        # Helperfunction that creates datetime object.

        return datetime.datetime.fromtimestamp(
            ms / 1000.0, tz=datetime.timezone.utc
        )

    async def start_candle_sockets(
        self, symbols: FrozenSet[str], client: AsyncClient, db: _Database
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes parsed candle to db.<_Pair>.calc_window_rolls(). #TODO aanpassen
        """

        bm = BinanceSocketManager(client)
        chanels = [s.lower() + "@kline_1m" for s in symbols]
        ms = bm.multiplex_socket(chanels)
        async with ms as stream:
            while self.shutdown_flag == False:
                msg = await stream.recv()
                symbol = msg["data"]["s"]
                await self.q.put((symbol, None, msg))

    def parse_candle(self, raw: Dict) -> Candle:
        """Takes raw candle data from a single candle and returns a Candle object."""

        d = raw["data"]["k"]
        return Candle(
            event_time=self.ms_to_datetime(int(raw["data"]["E"])),
            symbol=raw["data"]["s"],
            open_time=self.ms_to_datetime(int(d["t"])),
            close_time=self.ms_to_datetime(int(d["T"])),
            is_closed=bool(d["x"]),
            open_price=float(d["o"]),
            close_price=float(d["c"]),
            high_price=float(d["h"]),
            low_price=float(d["l"]),
            base_asset_volume=float(d["v"]),
            n_trades=int(d["n"]),
            quote_asset_volume=float(d["q"]),
            taker_buy_base_asset_volume=float(d["V"]),
            taker_buy_quote_asset_volume=float(d["Q"]),
        )

    async def start_user_socket(
        self, client: AsyncClient, db: _Database
    ) -> None:
        """Starts a websocket that listens to user events."""

        pass  # TODO

    def parse_user_event(self, event: Any) -> UserEvent:

        """Parses a message from a user socket. This message is one of
        the following events:
        1) Account update
        2) Order update
        3) Trade update
        """

        pass  # TODO
