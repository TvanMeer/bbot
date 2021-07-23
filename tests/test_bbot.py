import pytest

from bbot.bbot import Bot
from bbot.asyncbot import _AsyncBot
from bbot.options import Options


@pytest.fixture()
def bot():
    # Bot with default demo options.
    return Bot(options=Options())


def test_stop():
    pass


def test_create_client(bot):
    assert isinstance(bot.options, Options)
    assert isinstance(bot._bot, _AsyncBot)
