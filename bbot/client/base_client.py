'''

Abstract interface for all clients

Only Binance client is implemented.

'''

import abc
import asyncio
from typing import Any, Dict, List, Set

from ..data import database
from .. import options

class BaseClient(metaclass=abc.ABCMeta):

    def __init__(self, options: options.Options):

        self.options = options
        self.db = self._create_database(self.options)

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.client = self._create_async_client(self.options)

        raw      = self._download_all_symbols(self.client)
        parsed   = self._parse_all_symbols(raw)
        filtered = self.db._filter_symbols(parsed)

        self._start_coroutines(filtered, self.client)


    def _create_database(self, options: options.Options) -> database.Database:
        return database.DataBase(options)

    @abc.abstractmethod
    async def _create_async_client(options: options.Options) -> Any:
        ...
    
    @abc.abstractmethod
    async def _download_all_symbols(self, client: Any) -> Any:
        ...

    @abc.abstractmethod
    def _parse_all_symbols(raw: Any) -> Set[str]:
        ...
    
    async def _start_coroutines(self, symbols: Set[str], client: Any) -> None:
        __hist = asyncio.create_task(self._download_history(client))
        __cs   = asyncio.create_task(self._start_candle_sockets(client))
        __us   = asyncio.create_task(self._start_user_socket(client))
        await __cs, __hist, __us

    @abc.abstractmethod
    async def _download_history(client: Any) -> Any:
        ...

    @abc.abstractmethod
    def _parse_history(raw: Any) -> List[Dict[str, float]]:
        ...

    @abc.abstractmethod
    async def _start_candle_sockets(client: Any) -> None:
        ...

    @abc.abstractmethod
    def _parse_candle(raw: Dict) -> Dict:
        ...

    @abc.abstractmethod
    async def _start_user_socket(client: Any) -> None:
        ...

    @abc.abstractmethod
    def _parse_user_event(event: Any) -> Dict:
        ...