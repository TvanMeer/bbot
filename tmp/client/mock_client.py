import asyncio
from typing import Dict, FrozenSet, List
from random import choice, randint, random
from binance.client import AsyncClient

from bbot.client.base_client import _BaseClient
from bbot.data.user_event import UserEvent
from bbot.options import Options


class AsyncClientMock:
    pass  # TODO


class HistoryDownloaderMock:
    """Helperclass: A generator that produces fake historical candles in the format
    provided by python-binance.
    """

    def __init__(self, options, interval):
        self.options = options
        self.interval = interval
        self.c = [
            1624934520000,
            34406.08000000,
            34437.11000000,
            34395.07000000,
            34431.47000000,
            18.20600800,
            1624934579999,
            626663.26924604,
            560,
            10.84483500,
            373333.75765970,
            0,
        ]
        self.bullish = 0

    def __iter__(self):

        # Return self.c
        cop = self.c.copy()
        for i in [1, 2, 3, 4, 5, 7, 9, 10]:
            cop[i] = str(self.c[i])

        yield cop

        # Generate new fake historical candle by overwriting self.c
        self.c[0] += self.options._possible_intervals[self.interval]
        self.c[1] = self.c[4]
        if self.bullish > -1:
            self.c[2:5] *= 1.0001
        else:
            self.c[2:5] *= 0.9999
        self.c[5] = round(random.normal(1, 5), 8)
        self.c[6] += self.options._possible_intervals[self.interval]
        self.c[7] = round(random.normal(100000, 500000), 8)
        self.c[8] = randint(50, 500)
        self.c[9] = round(random.normal(1, 5), 8)
        self.c[10] = round(random.normal(30000, 150000), 8)

        if self.bullish > -1:
            self.bullish += 1
            if self.bullish > random.uniform(1, 100):
                self.bullish = -1
        else:
            self.bullish -= 1
            if self.bullish < random.uniform(-100, -1):
                self.bullish = 0


class CandleSocketsMock:
    """Helperclass: A generator that produces fake candles in the format provided by python-binance"""

    def __init__(self, selected_symbols: FrozenSet):
        self.selected_symbols = selected_symbols
        self.c = {
            "stream": "btcusdt@kline_1m",
            "data": {
                "e": "kline",
                "E": 1624935608626,
                "s": "BTCUSDT",
                "k": {
                    "t": 1624935600000,
                    "T": 1624935659999,
                    "s": "BTCUSDT",
                    "i": "1m",
                    "f": 123456789,
                    "L": 123456789,
                    "o": 10250.12000000,
                    "c": 10500.12000000,
                    "h": 10750.12000000,
                    "l": 10000.12000000,
                    "v": 4.12345600,
                    "n": 123,
                    "x": False,
                    "q": 123456.67891234,
                    "V": 1.23456789,
                    "Q": 56789.12345678,
                    "B": "0",
                },
            },
        }
        self.bullish = 0
        self.closed = 0

    # Update field helper funcs
    def u(self, field, val):
        self.c["data"]["k"][field] = val

    def a(self, field, val):
        self.c["data"]["k"][field] += val

    def m(self, field, val):
        self.c["data"]["k"][field] *= val

    def __iter__(self):

        cop = self.c.copy()
        for f in ["o", "c", "h", "l", "v", "q", "V", "Q"]:
            cop["data"]["k"][f] = str(self.c["data"]["k"][f])

        yield cop

        # Generate a new fake candle by overwriting last candle self.c
        symbol = choice(self.selected_symbols)
        self.c["stream"] = symbol + "@kline_1m"
        self.c["data"]["E"] += 2000
        self.c["data"]["s"] = symbol
        self.c["data"]["k"]["t"] += 60000
        self.c["data"]["k"]["T"] += 60000
        self.c["data"]["k"]["s"] = symbol
        self.c["data"]["k"]["o"] = self.c["data"]["k"]["c"]

        [
            self.m(f, 1.0001) if self.bullish > -1 else self.m(f, 0.9999)
            for f in ["c", "h", "l"]
        ]

        self.u("v", round(random.normal(1, 5), 8))
        self.u("n", randint(50, 500))

        if self.closed < 30:
            self.u("x", False)
            self.closed += 1
        else:
            self.u("x", True)
            self.closed = 0

        self.u("q", round(random.normal(100000, 500000), 8))
        self.u("V", round(random.normal(1, 5), 8))
        self.u("Q", round(random.normal(30000, 150000), 8))

        if self.bullish > -1:
            self.bullish += 1
            if self.bullish > random.uniform(1, 100):
                self.bullish = -1
        else:
            self.bullish -= 1
            if self.bullish < random.uniform(-100, -1):
                self.bullish = 0


class FakeClient(_BaseClient):
    """A mock implementation of abstract class _BaseClient."""

    def __init__(self, options):
        super().__init__(options)

        # State vars
        self.hist_candles_downloaded = 0

    async def create_async_client(self, options: Options) -> Any:
        """Returns <some> client object that is a coroutine.
        In case of Binance this is the python-binance.AsyncClient object.
        """
        # TODO
        return AsyncClientMock()

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

        for s in selected_symbols:
            for t in window_options.keys():
                candles = iter(HistoryDownloaderMock(self.options, t))
                while self.hist_candles_downloaded < window_options[t]:
                    self.q.put((next(candles), s, t))
                    self.hist_candles_downloaded += 1
                self.hist_candles_downloaded = 0
                await asyncio.sleep(2)

    async def start_candle_sockets(
        self, selected_symbols: FrozenSet[str], client: AsyncClient
    ) -> None:
        """Starts one or multiple websockets to stream candlestick data.
        Each socket streams data related to one pair. Only time interval
        1 minute is streamed. Other intervals are calculated on the fly later.
        Passes each incoming message in the queue.
        """

        candles = iter(CandleSocketsMock(selected_symbols))
        while True:
            candle = next(candles)
            symbol = candle["data"]["s"]
            self.q.put((candle, symbol, "1m"))
            await asyncio.sleep(2)

    def parse_new_candle(self, payload: Dict) -> Dict[str, float]:
        """Takes data of a single candle as provided by a websocket and returns a
        dict representing a single candle.
        """

        # TODO: all this code is python-binance specific
        # Get these functions out
        # 1. implement all funcs in this file
        # 2. implement logging.debug
        # 3. copy funcs to binance-client
        # 4. implement test_binance_client
        # 5. implement test_base_client
        d = payload["data"]["k"]
        return {
            "open_time": float(d["t"]),
            "open": float(d["o"]),
            "high": float(d["h"]),
            "low": float(d["l"]),
            "close": float(d["c"]),
            "volume": float(d["v"]),
            "close_time": float(d["T"]),
            "qa_volume": float(d["q"]),
            "n_trades": float(d["n"]),
            "tbba_volume": float(d["V"]),
            "tbqa_volume": float(d["Q"]),
            "corrupt": False,
        }

    async def start_user_socket(self, client: AsyncClient) -> None:
        """Starts a websocket that listens to user events.
        These user events are passed to the queue as raw data payload.
        """
        pass
        # TODO

    def parse_user_event(self, event: Dict) -> UserEvent:
        """Parses a message received from the user socket.
        This message is one of the following events:
        1) Account update
        2) Order update
        3) Trade update
        """

        return UserEvent()
        # TODO
