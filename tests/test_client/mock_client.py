import asyncio
from typing import Dict, FrozenSet, List
from binance.client import AsyncClient

from bbot.client.base_client import _BaseClient
from bbot.client.binance_client import _BinanceClient
from bbot.data.user_event import UserEvent
from bbot.options import Options


class MockClient(_BaseClient):
    """A mock implementation of abstract class _BaseClient."""

    def __init__(self, options):
        super().__init__(options)

        # State vars
        self.hist_candles_parsed = -1

    async def create_async_client(self, options: Options) -> AsyncClient:
        """Returns a python-binance.AsyncClient object."""

        return await AsyncClient.create(
            api_key=options._api_key, api_secret=options._api_secret
        )

    async def download_all_symbols(self, client: AsyncClient) -> List[Dict]:
        """Returns ticker list containing all symbols traded on Binance."""

        await asyncio.sleep(0.1)
        return [
            {"symbol": "BTCUSDT", "price": "0.22540000"},
            {"symbol": "ADAUSDT", "price": "0.02093000"},
            {"symbol": "BTCUSDC", "price": "0.70170000"},
            {"symbol": "XRPBTC", "price": "12345.74780000"},
            {"symbol": "BTCxxxxxUSDT", "price": "34437.11000000"},
        ]

    def parse_all_symbols(self, payload: List[Dict]) -> FrozenSet[str]:
        """Parses all symbols of pairs traded on Binance.
        Payload is list of tickers.
        """

        return frozenset(
            {"BTCUSDT", "ADAUSDT", "BTCUSDC", "XRPBTC", "BTCxxxxxUSDT"}
        )

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

        candles = [
            [
                1624934520000,
                "34406.08000000",
                "34437.11000000",
                "34395.07000000",
                "34431.47000000",
                "18.20600800",
                1624934579999,
                "626663.26924604",
                560,
                "10.84483500",
                "373333.75765970",
                "0",
            ],
            [
                1624934580000,
                "34431.47000000",
                "34440.86000000",
                "34431.47000000",
                "34438.75000000",
                "1.56972700",
                1624934639999,
                "54055.33589430",
                61,
                "1.32232600",
                "45535.39363053",
                "0",
            ],
        ]

        for c in candles:
            await asyncio.sleep(2)
            self.q.put((c, "BTCUSDT", "1m"))

    def parse_historical_candle(self, payload: List) -> Dict[str, float]:
        """Takes historical data of a single candle as returned by a rest-API call.
        Returns a dict that represents a single candle.
        """

        self.hist_candles_parsed += 1
        if self.hist_candles_parsed == 0:

            return {
                "open_time": float(1624934520000),
                "open": float("34406.08000000"),
                "high": float("34437.11000000"),
                "low": float("34395.07000000"),
                "close": float("34431.47000000"),
                "volume": float("18.20600800"),
                "close_time": float(1624934579999),
                "qa_volume": float("626663.26924604"),
                "n_trades": float(560),
                "tbba_volume": float("10.84483500"),
                "tbqa_volume": "373333.75765970",
                "missing": False,
            }
        else:
            return {
                "open_time": float(1624934580000),
                "open": float("34431.47000000"),
                "high": float("34440.86000000"),
                "low": float("34431.47000000"),
                "close": float("34431.47000000"),
                "volume": float("34438.75000000"),
                "close_time": float(1624934639999),
                "qa_volume": float("54055.33589430"),
                "n_trades": float(61),
                "tbba_volume": float("1.32232600"),
                "tbqa_volume": "45535.39363053",
                "missing": False,
            }

    async def start_candle_sockets(
        self, selected_symbols: FrozenSet[str], client: AsyncClient
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes each incoming message in the queue.
        """

        # TODO

    def parse_new_candle(self, payload: Dict) -> Dict[str, float]:
        """Takes data of a single candle as provided by a websocket and returns a
        dict representing a single candle.
        """

        return  # TODO

    async def start_user_socket(self, client: AsyncClient) -> None:
        """Starts a websocket that listens to user events.
        These user events are passed to the queue as raw data payload.
        """

        # TODO

    def parse_user_event(self, event: Dict) -> UserEvent:
        """Parses a message received from the user socket.
        This message is one of the following events:
        1) Account update
        2) Order update
        3) Trade update
        """

        return  # TODO
