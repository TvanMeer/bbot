from binance.client import AsyncClient
import asyncio
import pytest
import json

from bbot.asyncbot import _AsyncBot
from bbot.options import Options


@pytest.fixture()
def asyncbot():
    with open("credentials.json", "r") as authfile:
        data = authfile.read()
        c = json.loads(data)
        opt = Options(api_key=c["key"], api_secret=c["secret"])
        return _AsyncBot(opt)


def test_init(asyncbot):
    assert isinstance(asyncbot.options, Options)
    assert asyncbot.candles == {}
    assert asyncbot.user_events == []
    assert isinstance(asyncbot.loop, asyncio.BaseEventLoop)
    assert asyncbot.loop == asyncio.get_event_loop()
    assert isinstance(asyncbot.q, asyncio.Queue)


@pytest.mark.asyncio
async def test_prepare():
    pass


@pytest.mark.asyncio
async def test_download_all_symbols(asyncbot):

    asyncbot.client = await AsyncClient.create()
    symbols = await asyncbot.download_all_symbols(asyncbot.client)
    assert isinstance(symbols, set)
    for member in symbols:
        assert isinstance(member, str)
    assert len(symbols) > 500

    await asyncbot.client.close_connection()


def test_select_symbols(asyncbot):
    def x(b, q):
        all_symbols = {"BTCUSDT", "BTCUSDC", "XRPUSDT", "ADAUSDT", "BTCxUSDT"}
        opt = Options()
        opt.base_assets = b
        opt.quote_assets = q
        s = asyncbot.select_symbols(all_symbols, opt)
        return s

    assert x("BTC", "USDT") == {
        "BTCUSDT",
    }
    print(x("BTC", "*"))
    assert x("BTC", "*") == {"BTCUSDT", "BTCUSDC", "BTCxUSDT"}
    assert x("*", "USDT") == {"BTCUSDT", "XRPUSDT", "ADAUSDT", "BTCxUSDT"}
    assert x(["XRP", "ADA"], "USDT") == {"XRPUSDT", "ADAUSDT"}
    assert x(["XRP", "ADA"], "USDC") == set()
    assert x("*", "*") == {
        "BTCUSDT",
        "BTCUSDC",
        "XRPUSDT",
        "ADAUSDT",
        "BTCxUSDT",
    }


@pytest.mark.asyncio
async def test_download_exchange_info(asyncbot):

    asyncbot.client = await AsyncClient.create()
    info = await asyncbot.download_exchange_info(asyncbot.client)
    assert isinstance(info, dict)
    assert info["timezone"] == "UTC"
    assert info["serverTime"] > 1627014234650
    # print(json.dumps(info, indent=2))

    await asyncbot.client.close_connection()


@pytest.mark.asyncio
async def test_download_account_info(asyncbot):

    asyncbot.client = await AsyncClient.create(
        api_key=asyncbot.options.api_key,
        api_secret=asyncbot.options.api_secret,
        testnet=True,
    )
    info = await asyncbot.download_account_info(asyncbot.client)
    assert isinstance(info, dict)
    assert info["canTrade"] == True
    assert info["permissions"] == ["SPOT"]
    print(json.dumps(info, indent=2))
    await asyncbot.client.close_connection()


@pytest.mark.asyncio
async def test_start_loops(asyncbot):
    pass
