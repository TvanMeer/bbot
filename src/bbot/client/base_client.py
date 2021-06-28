import asyncio
from abc import abstractmethod, ABCMeta
from typing import Any, Dict, FrozenSet

from ..data.user_event import UserEvent
from ..options import Options


class _BaseClient(metaclass=ABCMeta):
    """Abstract interface for all exchange clients.
    Only for Binance a client is implemented.

    Usage:
    client = _BaseClient(options)   # instantiate _BinanceClient
    client.start()
    client.start_loops()
    ...
    client.stop()
    """

    def __init__(self, options: Options) -> None:
        self.options = options
        self.shutdown_flag = False
        self.finished_history_download = set()

        self.candles = {}
        self.all_symbols = set()
        self.selected_symbols = set()
        self.user_events = []

    def start(self) -> None:
        """All bootstrapping logic of _BaseClient is defined here.
        _BaseClient is spawned in a separate process.
        1) Create new asyncio event loop
        2) Initialize some AsyncClient object
        3) Discover all pairs on the exchange and make a selection
        4) Prepare self.candles
        5) Start the following loops concurrently:
        -Start data consumer                                      (infinite loop)
        -Start historical candlestick data downloads
        -Start websockets that stream realtime candlestick data   (infinite loop)
        -Start a websocket that listens to user events            (infinite loop)
        """

        # 1
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.q = asyncio.Queue()

        # 2
        self.client = self.create_async_client(self.options)

        # 3
        payload = self.download_all_symbols(self.client)
        self.all_symbols = self.parse_all_symbols(payload)
        self.selected_symbols = self.filter_symbols(
            self.all_symbols, self.options
        )

        # 4
        for sym in self.selected_symbols:
            for iv in self.options.windows.keys():
                self.candles[sym][iv] = []

        # 5
        # Start downloads and streams by calling client.start_loops()
        # from outside this class.

    def stop(self) -> None:
        """Shutdown client."""

        self.shutdown_flag = True
        self.loop.close()
        # process.join() ?

    @abstractmethod
    async def create_async_client(self, options: Options) -> Any:
        """Returns <some> client object that is a coroutine.
        In case of Binance this is the python-binance.AsyncClient object.
        """

    def start_loops(self) -> None:
        """Calls self.start_coroutines().
        This function should be called in class Bot, outside of this class.
        """

        self.loop.run_until_complete(self.start_coroutines())

    async def start_coroutines(self) -> None:
        """Starts concurrent loops."""

        co = asyncio.create_task(self.start_consumer())
        cs = asyncio.create_task(
            self.start_candle_sockets(self.selected_symbols, self.client)
        )
        hs = asyncio.create_task(
            self.download_history(
                self.selected_symbols,
                self.options.windows,
                self.client,
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
        These messages are of type Tuple(payload, symbol, interval).
        A message can be an historical candle, new candle or user event.

        All logic of data processing is specified here.
        """

        while self.shutdown_flag == False:
            payload, symbol, interval = await self.q.get()
            if symbol is None:
                # User event
                ue = self.parse_user_event(payload)
                self.user_events.append(ue)
            elif interval is not None:
                # Historical candle
                hc = self.parse_historical_candle(payload)
                vc = self.validate_historical_candle(hc, symbol, interval)
                self.candles[symbol][interval].append(vc)
                if (
                    len(self.candles[symbol][interval])
                    >= self.options.windows[interval]
                ):
                    self.finished_history_download.add((symbol, interval))
            else:
                # New candle
                if (symbol, interval) not in self.finished_history_download:
                    continue
                nc = self.parse_new_candle(payload)
                vc = self.validate_new_candle(nc, symbol)
                rolls = self.calc_window_rolls(nc, symbol)
                updates = set(self.options.windows.keys()).difference(rolls)
                # Opening candle
                for iv in rolls:
                    self.candles[symbol][iv].append(vc)
                    del self.candles[symbol][iv][0]
                # Candle update
                for iv in updates:
                    self.update_candle(nc, symbol, iv)

    @abstractmethod
    async def download_all_symbols(self, client: Any) -> Any:
        """Downloads <some data> that contains all symbols of the
        pairs that are traded at the exchange. An example of a symbol
        is 'BTCUSDT'. Returns this data as provided by the API.
        """

    @abstractmethod
    def parse_all_symbols(self, payload: Any) -> FrozenSet[str]:
        """Parses all symbols of pairs traded at the exchange from <some data>."""

    def filter_symbols(
        self, all_symbols: FrozenSet[str], options: Options
    ) -> FrozenSet[str]:
        """Filters symbols that have as base asset, one specified in options.base_assets,
        or as quote asset, one specified in options.quote_assets.
        Returns selected symbols.
        """
        pass  # TODO

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
        The 2 second interval is skipped, because exchanges do not support that.
        Iterates through each downloaded window and passes single candles to the queue,
        starting with the oldest and ending with the most recent.
        """

    @abstractmethod
    def parse_historical_candle(self, payload: Any) -> Dict[str, float]:
        """Takes historical data of a single candle as returned by a rest-API call.
        Returns a dict that represents a single candle.
        """

    def validate_historical_candle(
        self, payload: Dict[str, float], symbol: str, interval: str
    ) -> Dict[str, float]:
        """Validates an historical candle.
        Sets candle["missing"] = True if any data leakage/ corruption is found.
        Returns the same candle.
        """
        pass  # TODO

    @abstractmethod
    async def start_candle_sockets(
        self, symbols: FrozenSet[str], client: Any
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes each incoming message in the queue.
        """

    @abstractmethod
    def parse_new_candle(self, payload: Any) -> Dict[str, float]:
        """Takes data of a single candle as provided by a websocket and returns a
        dict representing a single candle.
        """

    def calc_window_rolls(
        self, candle: Dict[str, float], symbol: str
    ) -> FrozenSet[str]:
        """Iterates through all windows, then calculates if candle is the
        first update (open) of a new candle in window.
        Returns a set of intervals, that indicate to which windows candle
        needs to be appended.
        Intervals that are *not* in this set need to be updated instead.
        """
        pass  # TODO

    def validate_new_candle(
        self, candle: Dict[str, float], symbol: str
    ) -> Dict[str, float]:
        """Validates a new candle, coming from a websocket.
        Validates for both opening candles and candle updates.
        Sets candle["missing"] = True if any data leakage/ corruption is found.
        Returns the same candle.
        """
        pass  # TODO

    def update_candle(
        self, candle: Dict[str, float], symbol: str, interval: str
    ) -> None:
        """Updates the last candle in de corresponding window in self.candles."""
        pass  # TODO

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
