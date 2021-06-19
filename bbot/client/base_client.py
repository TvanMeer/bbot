import abc
import asyncio
from typing import Any, Dict, List, Set


from ..data.candle     import Candle
from ..data.database   import Database
from ..data.user_event import UserEvent
from ..options         import Options

class BaseClient(metaclass=abc.ABCMeta):
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
        self.db = self._create_database(self.options)
        # 2
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # 3
        self.client = self._create_async_client(self.options)
        # 4
        raw      = self._download_all_symbols(self.client)
        parsed   = self._parse_all_symbols(raw)
        filtered = self.db._filter_symbols(parsed)
        # 5
        self._start_coroutines(filtered, self.client)


    def _create_database(self, options: Options) -> Database:
        """Returns a Database object that contains all data.
        It needs to be initialized in the separate process where
        the API client lives. Not in the main process.
        """
        return Database(options)

    @abc.abstractmethod
    async def _create_async_client(options: Options) -> Any:
        """Returns some client object. In the case of Binance this
        is the python-binance.AsyncClient object. This object is
        passed as an argument in all functions that do API calls.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    async def _download_all_symbols(self, client: Any) -> Any:
        """Downloads *some data* that contains all symbols of the 
        pairs being traded at the exchange. An example of a symbol 
        is 'BTCUSDT'. Return this data as provided by the API.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_all_symbols(raw: Any) -> Set[str]:
        """Filters all sybols from the data that is obtained 
        with _download_all_symbols().
        """
        raise NotImplementedError
    
    async def _start_coroutines(self, symbols: Set[str], client: Any) -> None:
        _hist = asyncio.create_task(self._download_history(symbols, client))
        _cs   = asyncio.create_task(self._start_candle_sockets(symbols, client))
        _us   = asyncio.create_task(self._start_user_socket(client))
        await _cs, _hist, _us

    @abc.abstractmethod
    async def _download_history(symbols: Set[str], client: Any) -> Any:
        """Returns historical candlestick data, as raw data in the
        format provided by the API.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_history(raw: Any) -> List[Candle]:
        """Takes raw historical candlestick data from _download_history()
        and transforms it to a list of Candle objects.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def _start_candle_sockets(symbols: Set[str], client: Any) -> None:
        """Starts one or multiple websockets that stream candlestick data."""
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_candle(raw: Dict) -> Candle:
        """Takes raw data of a single candle and returns a Candle object."""
        raise NotImplementedError

    @abc.abstractmethod
    async def _start_user_socket(client: Any) -> None:
        """Starts a websocket that listens to user events."""
        raise NotImplementedError

    @abc.abstractmethod
    def _parse_user_event(event: Any) -> UserEvent:
        """Parses a message from a user socket. This message is one of
        the following events:
        1) Account update
        2) Order update
        3) Trade update
        """
        raise NotImplementedError