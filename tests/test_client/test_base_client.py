import asyncio
import time
from datetime import datetime
from typing import Any, FrozenSet
import pytest

from bbot.client.base_client import _BaseClient
from bbot.data.user_event import UserEvent
from bbot.options import Options


@pytest.fixture
def options():
    return Options()


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


# @pytest.fixture
# def event_loop():
#    loop = asyncio.new_event_loop()
#    asyncio.set_event_loop(loop)
#    yield loop
#    loop.close()

# class TestClient(_BaseClient):

#    # A mock client implementation:
#    def __init__(self, options: Options()):
#        super().__init__(options)

# @pytest.fixture
# def client(options):
#    return TestClient(options)


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
