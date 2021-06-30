import asyncio
import time
from datetime import datetime
from typing import Any, FrozenSet
from binance.client import AsyncClient
import pytest

from bbot.client.base_client import _BaseClient
from bbot.data.user_event import UserEvent
from bbot.options import Options

from .test_binance_client import all_tickers, history_1m, options, async_client


@pytest.fixture
def all_symbols():
    return frozenset(
        ["BTCUSDT", "ADAUSDT", "BTCUSDC", "XRPBTC", "BTCxxxxxUSDT"]
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





@pytest.fixture
def test_client_orig(options, async_client, all_tickers, all_symbols, history_1m):
    class TestClient(_BaseClient):
        """A mock client implementation."""

        def __init__(self, options):
            super().__init__(options)

        async def create_async_client(self, options):
            await asyncio.sleep(0.0001)
            return async_client

        async def download_all_symbols(self, client):
            await asyncio.sleep(0.0001)
            return all_tickers

        def parse_all_symbols(self, payload):
            return all_symbols

        async def download_history(self, selected_symbols, window_options, client):
            await asyncio.sleep(0.5)
            return history_1m

        def parse_historical_candle(self, payload):
            pass  # TODO

        async def start_candle_sockets(self, symbols, client):
            await asyncio.sleep(1)

        def parse_new_candle(self, payload):
            pass  # TODO

        async def start_user_socket(self, client):
            await asyncio.sleep(1)

        def parse_user_event(self, event):
            pass  # TODO


    return TestClient(options)

@pytest.fixture
def event_loop():
   loop = asyncio.new_event_loop()
   asyncio.set_event_loop(loop)
   yield loop
   loop.close()

@pytest.fixture
def test_client(test_client_orig, event_loop):
   test_client_orig.loop = event_loop
   return test_client_orig


# Unit tests ----------------------------------------------------------


def test_init(options):
    pass


def test_start():
    pass


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
