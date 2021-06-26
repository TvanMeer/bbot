import asyncio
import pytest

from binance import AsyncClient

from bbot.client.binance_client import _BinanceClient
from bbot.data.database import _Database
from bbot.options import Options


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def options():
    return Options()


@pytest.fixture
def binance_client(options):
    return _BinanceClient(options)


def test_init(binance_client):
    assert isinstance(binance_client.options, Options)
    assert isinstance(binance_client.db, _Database)
    assert isinstance(binance_client.loop, asyncio.BaseEventLoop)
    assert isinstance(binance_client.client, AsyncClient)
    assert isinstance(binance_client.db.all_symbols, frozenset)
    assert isinstance(binance_client.db.selected_symbols, frozenset)
    assert binance_client.shutdown_flag == False


def test_shutdown(binance_client):
    binance_client.shutdown()
    assert binance_client.shutdown_flag == True
    # TODO


@pytest.mark.asyncio
async def test_create_async_client(binance_client, options):
    client = await binance_client.create_async_client(options)
    assert isinstance(client, AsyncClient)


@pytest.mark.asyncio
async def test_download_all_symbols(binance_client):
    client = await binance_client.create_async_client(options)
    tickers = await binance_client.download_all_symbols(client)
    assert isinstance(tickers, list)
    for t in tickers:
        assert isinstance(t, dict)
        assert isinstance(t[0], str)
        assert len(tickers) > 500


def test_parse_all_symbols(binance_client):
    client = binance_client.create_async_client(options)
    tickers = binance_client.download_all_symbols(client)
    parsed = binance_client.parse_all_symbols(tickers)
    assert len(parsed) == len(tickers)
    assert isinstance(parsed, frozenset)


@pytest.mark.asyncio
async def test_download_history(binance_client):
    pass  # TODO


def test_to_timestring(binance_client):
    assert binance_client.to_timestring("1m", 1000) == "1000 minutes ago UTC"
    assert binance_client.to_timestring("15m", 100) == "1500 minutes ago UTC"
    assert binance_client.to_timestring("1h", 100) == "100 hours ago UTC"
    assert binance_client.to_timestring("1d", 100) == "100 days ago UTC"
    assert binance_client.to_timestring("1w", 100) == "100 weeks ago UTC"
    with pytest.raises(Exception):
        binance_client.to_timestring("foo", 100)


def test_parse_historical_candle(binance_client):
    pass  # TODO


def test_ms_to_datetime(binance_client):
    pass  # TODO


@pytest.mark.asyncio
async def test_start_candle_sockets(binance_client):
    pass  # TODO


def test_parse_candle(binance_client):
    pass  # TODO


@pytest.mark.asyncio
async def test_start_user_socket(binance_client):
    pass  # TODO


def test_parse_user_event(binance_client):
    pass  # TODO
