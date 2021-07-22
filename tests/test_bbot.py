import pytest

from bbot.bbot import Bot
from bbot.asyncbot import _AsyncBot
from bbot.options import Options


@pytest.fixture(autouse=True)
def bot():
    # Bot with default demo options.
    return Bot(options=Options())


def test_stop():
    pass


def test_create_client():
    assert bot.options == Options()
    assert bot._bot is _AsyncBot
