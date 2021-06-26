import asyncio
from abc import abstractmethod, ABCMeta
from typing import Any, FrozenSet


from ..data.candle import Candle
from ..data.database import _Database
from ..data.user_event import UserEvent
from ..options import Options


class _BaseClient(metaclass=ABCMeta):
    """Abstract interface for all exchange clients.
    Only for Binance a client is implemented.
    """

    def __init__(self, options: Options):
        """All bootstrapping logic of client is defined here.
        Client is spawned in a separate process.
        1) Initialize Database
        2) Create event loop
        3) Initialize client object
        4) Discover all pairs on the exchange and make a selection
        5) Start all downloads and streams
        """

        # 1
        self.options = options
        self.db = self.create_database(self.options)

        # 2
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # 3
        self.client = self.create_async_client(self.options)

        # 4
        raw = self.download_all_symbols(self.client)

        parsed = self.parse_all_symbols(raw)
        self.db.all_symbols = parsed

        filtered = self.db.filter_symbols(parsed)
        self.db.selected_symbols = filtered

        # 5
        # Start downloads and streams by calling client.start()
        # from outside of this class.

    def create_database(self, options: Options) -> _Database:
        """Returns a _Database object that contains all data.
        It needs to be initialized in the separate process where
        the API client lives. Not in the main process.
        """

        return _Database(options)

    def start_loops(self):
        """Calls start_coroutines()."""
        self.loop.run_until_complete(
            self.start_coroutines(self.loop, self.db.selected_symbols, self.client, self.db)
        )

    async def start_coroutines(
        self, loop: asyncio.BaseEventLoop, symbols: FrozenSet[str], client: Any, db: _Database
    ) -> None:
        """Starts concurrent downloads and streams."""

        hist = asyncio.create_task(self.download_history(symbols, client, db))
        cs = asyncio.create_task(self.start_candle_sockets(symbols, client, db))
        us = asyncio.create_task(self.start_user_socket(client))
        try:
            await cs, hist, us
        except KeyboardInterrupt:
            print("Bbot interrupted...")
        finally:
            self.loop.close()
            print("Bbot shutdown...")

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown client."""

    @abstractmethod
    async def create_async_client(self, options: Options) -> Any:
        """Returns *some* client object. In case of Binance this
        is the python-binance.AsyncClient object. This object is
        passed as an argument in all functions that do API calls.
        """

    @abstractmethod
    async def download_all_symbols(self, client: Any) -> Any:
        """Downloads *some data* that contains all symbols of the
        pairs being traded at the exchange. An example of a symbol
        is 'BTCUSDT'. Return this data as provided by the API.
        """

    @abstractmethod
    def parse_all_symbols(self, raw: Any) -> FrozenSet[str]:
        """Filters and returns all symbols of pairs being traded
        at the exchange from raw data and returns them as a set.
        """

    @abstractmethod
    async def download_history(self, symbols: FrozenSet[str], client: Any, db: _Database) -> None:
        """Downloads all windows of historical candlestick data,
        as raw data in the format provided by the API. Then iterates through
        each window and passes candles one by one to self.parse_historical_candle().
        """

    @abstractmethod
    def parse_historical_candle(self, raw: Any, symbol: str, interval: str, db: _Database) -> None:
        """Takes single candle from raw historical candlestick data coming
        from self.download_history() and transforms it to a Candle object.
        Then passes this candle object to the corresponding Window instance in
        db.<Pair>.<Window>._add_historical_candle().
        """

    @abstractmethod
    async def start_candle_sockets(
        self, symbols: FrozenSet[str], client: Any, db: _Database
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes parsed candle to db.<_Pair>.calc_window_rolls().
        """

    @abstractmethod
    def parse_candle(self, raw: Any) -> Candle:
        """Takes raw data of a single candle and returns a Candle object."""

    @abstractmethod
    async def start_user_socket(self, client: Any) -> None:
        """Starts a websocket that listens to user events."""

    @abstractmethod
    def parse_user_event(self, event: Any) -> UserEvent:
        """Parses a message from a user socket. This message is one of
        the following events:
        1) Account update
        2) Order update
        3) Trade update
        """
