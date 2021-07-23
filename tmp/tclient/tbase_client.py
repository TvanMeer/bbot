import asyncio
from binance.client import AsyncClient
import pytest

from bbot.client.base_client import _BaseClient
from bbot.data.user_event import UserEvent
from bbot.options import Options

from .test_binance_client import (
    all_tickers,
    candle,
    history_1m,
    options,
    async_client,
    selected_symbols,
)

# TODO: BaseClientTest(_BaseClient, FakeClient)


@pytest.fixture
def all_symbols():
    return frozenset(
        {"BTCUSDT", "ADAUSDT", "BTCUSDC", "XRPBTC", "BTCxxxxxUSDT"}
    )


@pytest.fixture
def parsed_historical_candle():
    return {}  # TODO


@pytest.fixture
def symbol():
    return "BTCUSDT"


@pytest.fixture
def interval():
    return "1m"


@pytest.fixture
def parsed_new_candle():
    return {}  # TODO


@pytest.fixture(scope="module")
def testclient(
    options,
    async_client,
    all_tickers,
    all_symbols,
    history_1m,
    historical_candle,
    candle,
):
    class TestClient(_BaseClient):
        """A mock client implementation."""

        def __init__(self, options):
            super().__init__(options)

        async def create_async_client(self, async_client):
            await asyncio.sleep(0.0001)
            return async_client

        async def download_all_symbols(self, all_tickers):
            await asyncio.sleep(0.0001)
            return all_tickers

        def parse_all_symbols(self, all_symbols):
            return all_symbols

        async def download_history(self, history_1m):
            await asyncio.sleep(0.5)
            return history_1m

        def parse_historical_candle(self, parsed_historical_candle):
            return parsed_historical_candle

        async def start_candle_sockets(self, candle):
            while True:
                self.q.put(candle)
                await asyncio.sleep(2)

        def parse_new_candle(self, payload):
            pass  # TODO

        async def start_user_socket(self, client):
            await asyncio.sleep(1)

        def parse_user_event(self, event):
            pass  # TODO

    tc = TestClient(options)
    yield tc
    tc.stop()


# Unit tests ----------------------------------------------------------


def test_init(testclient):
    assert isinstance(testclient.options, Options)
    assert isinstance(testclient.shutdown_flag, bool)
    assert isinstance(testclient.finished_history_download, set)
    assert isinstance(testclient.candles, dict)
    assert isinstance(testclient.all_symbols, set)
    assert isinstance(testclient.selected_symbols, set)
    assert isinstance(testclient.user_events, list)


def test_start(testclient, all_symbols, selected_symbols):
    testclient.start()
    # assert isinstance(test_client.loop, asyncio.BaseEventLoop)
    # assert isinstance(test_client.q, asyncio.Queue)
    # assert isinstance(test_client, AsyncClient)
    # assert test_client.all_symbols == all_symbols
    # assert test_client.selected_symbols == selected_symbols
    # assert test_client.candles["BTCUSDT"]["1m"] == []
    # assert test_client.candles["BTCUSDT"]["15m"] == []


def test_stop():
    pass


def test_start_loops():
    pass


@pytest.mark.asyncio
async def test_start_coroutines():
    pass


@pytest.mark.asyncio
async def test_start_consumer():
    pass


def test_filter_symbols(all_symbols, options):
    pass


def test_validate_historical_candle(
    parsed_historical_candle, symbol, interval
):
    pass


def test_calc_window_rolls(parsed_new_candle, symbol):
    pass


def test_validate_new_candle(parsed_new_candle, symbol):
    pass


def test_update_candle(parsed_new_candle, symbol, interval):
    pass
