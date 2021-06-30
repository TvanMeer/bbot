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


class TestClient(_BaseClient):

    # A mock client implementation:
    def __init__(self, options: Options):
        super().__init__(options)

    def shutdown(self) -> None:
        pass

    async def create_async_client(self, options: Options) -> Any:
        return None

    async def download_all_symbols(self, client: Any) -> Any:
        return [{"BTCUSDT": 1000}, {"ADAUSDT": 165}]

    def parse_all_symbols(self, raw: Any) -> FrozenSet[str]:
        return frozenset(["BTCUSDT", "ADAUSDT"])

    async def download_history(
        self, symbols: FrozenSet[str], client: Any, db: _Database
    ) -> None:
        await asyncio.sleep(1)

    def parse_historical_candle(
        self, raw: Any, symbol: str, interval: str, db: _Database
    ) -> None:
        pass

    async def start_candle_sockets(
        self, symbols: FrozenSet[str], client: Any, db: _Database
    ) -> None:
        await asyncio.sleep(1)

    def parse_candle(self, raw: Any) -> Candle:
        return Candle(
            event_time=None,
            symbol="BTCUSDT",
            open_time=datetime,
            close_time=datetime,
            is_closed=False,
            open_price=123.0,
            close_price=123.0,
            high_price=123.0,
            low_price=123.0,
            base_asset_volume=10000.0,
            n_trades=10,
            quote_asset_volume=10000.0,
            taker_buy_base_asset_volume=10000.0,
            taker_buy_quote_asset_volume=10000.0,
        )

    async def start_user_socket(self, client: Any) -> None:
        await asyncio.sleep(1)

    def parse_user_event(self, event: Any) -> UserEvent:
        return UserEvent()

    async def start_consumer(self) -> None:
        await asyncio.sleep(1)


@pytest.fixture
def base_client(options):
    return TestClient(options)


@pytest.fixture
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


def test_init(options, base_client):
    assert isinstance(base_client.create_database(options), _Database)
    assert isinstance(base_client.loop, asyncio.BaseEventLoop)
    assert base_client.db.selected_symbols == frozenset(
        [
            "BTCUSDT",
        ]
    )


@pytest.mark.asyncio
async def test_start_coroutines(event_loop, base_client):

    assert event_loop.is_running()

    before = time.time()
    await base_client.start_coroutines(
        event_loop,
        base_client.db.selected_symbols,
        base_client.client,
        base_client.db,
    )
    after = time.time()
    assert after - before > 1 and after - before < 2
