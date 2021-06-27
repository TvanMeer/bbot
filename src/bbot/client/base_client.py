import asyncio
from abc import abstractmethod, ABCMeta
from typing import Any, Dict, FrozenSet


from ..data.candle import Candle
from ..data.database import Database
from ..data.user_event import UserEvent
from ..options import Options


class _BaseClient(metaclass=ABCMeta):
    """Abstract interface for all exchange clients.
    Only for Binance a client is implemented.

    Usage:
    client = _BaseClient(options)   # instantiate _BinanceClient
    client.start()
    client.start_loops()
    """

    def __init__(self, options: Options):
        self.options = options
        self.shutdown_flag = False

    def start(self):
        """All bootstrapping logic of _BaseClient is defined here.
        _BaseClient is spawned in a separate process.
        1) Initialize Database
        2) Create new asyncio event loop
        3) Initialize some AsyncClient object
        4) Discover all pairs on the exchange and make a selection
        5) Start the following loops concurrently:
        -Start data consumer                                      (infinite loop)
        -Start historical candlestick data downloads
        -Start websockets that stream realtime candlestick data   (infinite loop)
        -Start websocket that listens to user events              (infinite loop)
        """

        # 1
        self.db = self.create_new_database(self.options)

        # 2
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.q = asyncio.Queue()

        # 3
        self.client = self.create_async_client(self.options)

        # 4
        payload = self.download_all_symbols(self.client)
        parsed = self.parse_all_symbols(payload)
        self.db.all_symbols = parsed

        filtered = self.db._filter_symbols(parsed)
        self.db.selected_symbols = filtered

        # 5
        # Start downloads and streams by calling client.start_loops()
        # from outside this class.

    def stop(self) -> None:
        """Shutdown client."""

        self.shutdown_flag = True
        self.loop.close()
        # process.join() ?

    def create_new_database(self, options: Options) -> Database:
        """Returns a Database object that will contain all data.
        It needs to be initialized in the separate process where
        _BaseClient lives. Not in the main process in class Bot.
        """

        return Database(options)

    def start_loops(self) -> None:
        """Calls self.start_coroutines().
        This function should be called in class Bot, outside of this class.
        """

        self.loop.run_until_complete(self.start_coroutines())

    async def start_coroutines(self) -> None:
        """Starts concurrent loops."""

        co = asyncio.create_task(self.start_consumer())
        cs = asyncio.create_task(
            self.start_candle_sockets(self.db.selected_symbols, self.client)
        )
        hs = asyncio.create_task(
            self.download_history(
                self.db.selected_symbols, self.options.windows, self.client
            )
        )
        us = asyncio.create_task(self.start_user_socket(self.client))

        try:
            await co, cs, hs, us
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.stop()

    async def start_consumer(self) -> None:
        """Takes messages from the queue.
        These messages are of type Tuple(symbol, interval, payload).
        A message can be an historical candle, new candle or user event.

        Passes Candle object to one of these functions:
        -self.db.pairs[symbol].windows[interval]._add_historical_candle()
        -self.db.pairs[symbol]._calc_window_rolls().

        Appends UserEvent object to self.db.user_events.
        """

        while self.shutdown_flag == False:
            symbol, interval, payload = await self.q.get()
            if symbol is None:
                # User event
                ue = self.parse_user_event(payload)
                self.db.user_events.append(ue)
            elif interval is not None:
                # Historical candle
                hc = self.parse_historical_candle(payload)
                self.db.pairs[symbol].windows[interval]._add_historical_candle(
                    hc
                )
            else:
                # New candle
                c = self.parse_new_candle(payload)
                rolls = self.db.pairs[symbol]._calc_window_rolls(c)
                for iv in rolls:
                    self.db.pairs[symbol].windows[iv]._add_new_candle(c)
                updates = frozenset(self.options.windows.keys()).difference(
                    rolls
                )
                for iv in updates:
                    self.db.pairs[symbol].windows[iv]._update_candle(c)

    @abstractmethod
    async def create_async_client(self, options: Options) -> Any:
        """Returns <some> client object that is a coroutine.
        In case of Binance this is the python-binance.AsyncClient object.
        """

    @abstractmethod
    async def download_all_symbols(self, client: Any) -> Any:
        """Downloads <some data> that contains all symbols of the
        pairs that are traded at the exchange. An example of a symbol
        is 'BTCUSDT'. Returns this data as provided by the API.
        """

    @abstractmethod
    def parse_all_symbols(self, payload: Any) -> FrozenSet[str]:
        """Parses all symbols of pairs traded at the exchange from <some data>."""

    @abstractmethod
    async def download_history(
        self,
        selected_symbols: FrozenSet[str],
        window_options: Dict[str, int],
        client: Any,
    ) -> None:
        """Downloads historical candlestick data for all selected symbols.
        Each symbol can have multiple windows for different time intervals.
        The number of windows that are downloaded is n_symbols * n_intervals.
        Iterates through each downloaded window and passes single candles to the queue,
        starting with the oldest and ending with the most recent.
        """

    @abstractmethod
    def parse_historical_candle(self, payload: Any) -> Candle:
        """Takes historical data of a single candle as returned by a rest-API call.
        Returns a Candle object.
        """

    @abstractmethod
    async def start_candle_sockets(
        self, symbols: FrozenSet[str], client: Any
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes each incoming message to the queue.
        """

    @abstractmethod
    def parse_new_candle(self, payload: Any) -> Candle:
        """Takes data of a single candle as provided by a websocket and returns a Candle object."""

    @abstractmethod
    async def start_user_socket(self, client: Any) -> None:
        """Starts a websocket that listens to user events.
        These user events are passed to the queue as raw data payload.
        """

    @abstractmethod
    def parse_user_event(self, event: Any) -> UserEvent:
        """Parses a message received from the user socket.
        This message is one of the following events:
        1) Account update
        2) Order update
        3) Trade update
        """
