from typing import Dict, FrozenSet, List
from binance.client import AsyncClient

from .base_client import _BaseClient
from ..data.user_event import UserEvent
from ..options import Options


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
        """Returns ticker list containing all symbols traded on Binance."""

        return await client.get_all_tickers()

    def parse_all_symbols(self, payload: List[Dict]) -> FrozenSet[str]:
        """Parses all symbols of pairs traded on Binance.
        Payload is list of tickers.
        """

        all_symbols = set()
        [all_symbols.add(t["symbol"]) for t in payload]
        return frozenset(all_symbols)

    async def download_history(
        self,
        selected_symbols: FrozenSet[str],
        window_options: Dict[str, int],
        client: AsyncClient,
    ) -> None:
        """Downloads historical candlestick data for all selected symbols.
        Each symbol can have multiple windows for different time intervals.
        The number of windows that are downloaded is n_symbols * n_intervals.
        The 2 second interval is skipped, because exchanges do not support that.
        Iterates through each downloaded window and passes single candles to the queue,
        starting with the oldest and ending with the most recent.
        """

    def parse_historical_candle(self, payload: List) -> Dict[str, float]:
        """Takes historical data of a single candle as returned by a rest-API call.
        Returns a dict that represents a single candle.
        """

    async def start_candle_sockets(
        self, selected_symbols: FrozenSet[str], client: AsyncClient
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes each incoming message in the queue.
        """

    def parse_new_candle(self, payload: Dict) -> Dict[str, float]:
        """Takes data of a single candle as provided by a websocket and returns a
        dict representing a single candle.
        """

    async def start_user_socket(self, client: AsyncClient) -> None:
        """Starts a websocket that listens to user events.
        These user events are passed to the queue as raw data payload.
        """

    def parse_user_event(self, event: Dict) -> UserEvent:
        """Parses a message received from the user socket.
        This message is one of the following events:
        1) Account update
        2) Order update
        3) Trade update
        """
