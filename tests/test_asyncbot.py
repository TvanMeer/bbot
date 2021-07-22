import pytest

from bbot.asyncbot import _AsyncBot
from bbot.options import Options


@pytest.fixture(autouse=True)
def asyncbot():
    return _AsyncBot(Options())


def test_init():
    pass


@pytest.mark.asyncio
async def test_prepare():
    pass


@pytest.mark.asyncio
async def test_download_all_symbols():
    pass


def test_select_symbols():
    pass


@pytest.mark.asyncio
async def test_download_exchange_info():
    pass


@pytest.mark.asyncio
async def test_download_account_info():
    pass


@pytest.mark.asyncio
async def test_start_loops():
    pass
