import pytest

from bbot.bbot import Bot
from bbot.client.binance_client import _BinanceClient
from bbot.options import Options


@pytest.fixture
def bot():
    # Bot with default demo options.
    return Bot(options=Options())


def test_stop(bot):
    # assert bot.stop() == ...
    pass


def test__create_client(bot):
    assert bot._bc is _BinanceClient
    assert bot._bc == _BinanceClient(Options())
