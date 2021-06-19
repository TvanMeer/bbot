from typing import Any, Dict, List, Set
from binance import AsyncClient

from .base_client      import BaseClient
from ..options         import Options
from ..data.candle     import Candle
from ..data.user_event import UserEvent


class BinanceClient(BaseClient):
    """Binance client implementation"""
    
    def __init__(self, options: Options):
        """Starts bootstrapping logic in parents constructor."""
        super().__init__(options)

    async def _create_async_client(options: Options) -> AsyncClient:
        """Returns a python-binance.AsyncClient object."""
        client = await AsyncClient.create(api_key    = options.api_key, 
                                          api_secret = options.api_secret)
        return client

    async def _download_all_symbols(self, client: AsyncClient) -> List[Dict]:
        """Downloads ticker data that contains all symbols of trading pairs
        on Binance. This is a list of dicts with k=symbol and v=close_price.
        """
        raw = await client.get_all_tickers()
        return raw


    def _parse_all_symbols(raw: List[Dict]) -> Set[str]:
        """Filters symbols from Binance ticker data and returns a set 
        of symbols.
        """
        pass #TODO

    async def _download_history(symbols: Set[str], client: AsyncClient) -> List[List]:
        """Downloads historical candlestick data from Binance and returns
        this data without modifying it."""
        pass #TODO

    def _parse_history(raw: Any) -> List[Candle]:
        """Takes raw historical candlestick data from _download_history()
        and transforms it to a list of Candle objects.
        """
        pass #TODO

    async def _start_candle_sockets(symbols: Set[str], client: AsyncClient) -> None:
        """Starts one or multiple websockets that stream candlestick data.
        Each socket streams data related to one pair. Only time interval 
        1 minute is streamed. Other intervals are calculated on the fly later.
        """
        pass #TODO

    def _parse_candle(raw: Dict) -> Candle:
        """Takes raw candle data from a single candle and returns a Candle object."""
        pass #TODO

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