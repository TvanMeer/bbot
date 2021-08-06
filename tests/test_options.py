import pytest
from bbot.options import Options


@pytest.fixture
def options():
    return Options()


def test_api_key_secret(options):
    valid = [
        " ",
        "nsfXDBT5fTeYJX3QXECFyHzkQJfznfhY62bSI8AVYT4ITdofNbcImikj3tZVWUig",
    ]
    invalid = [
        "sfXDBT5fTeYJX3QXECFyHzkQJfznfhY62bSI8AVYT4ITdofNbcImikj3tZVWUig",
        "nsfXDBT5fTeYJX3QXECFyHzkQJfzn?hY62bSI8AVYT4ITdofNbcImikj3tZVWUig",
    ]
    for v in valid:
        options.api_key = v
        options.api_secret = v
        assert options._api_key == v
        assert options._api_secret == v
    for i in invalid:
        with pytest.raises(Exception):
            options.api_key = i
        with pytest.raises(Exception):
            options.api_secret = i


def test_mode(options):

    options.mode = "DEBUG"
    assert options._mode == "DEBUG"
    with pytest.raises(Exception):
        options.mode = "foo"


def test_assets(options):

    valid = ["btc", "ETH", "*", "USDT", ["XRP", "hot"]]
    expected = [["BTC"], ["ETH"], ["*"], ["USDT"], ["XRP", "HOT"]]
    invalid = [7, "abcdefghij", "b?c"]

    for v, e in zip(valid, expected):
        options.base_assets = v
        assert options._base_assets == e

    for v, e in zip(valid, expected):
        options.quote_assets = v
        assert options._quote_assets == e

    with pytest.raises(Exception):
        options.base_assets = "*"
        options.quote_assets = "*"

    for i in invalid:
        with pytest.raises(Exception):
            options.base_assets = i
        with pytest.raises(Exception):
            options.quote_assets = i


def test_windows(options):

    valid = {"2s": 200, "1m": 100}
    invalid = [
        {"2s": 200, "1m": 100.1},
        {"2s": 200, "1m": 502},
        {"2S": 200, "1m": 100},
        {"2s": 201, "1m": 100},
    ]

    options.windows = valid
    assert options._windows == valid

    for i in invalid:
        with pytest.raises(Exception):
            options.windows = i


def test_datasources(options):

    valid = ["candlestick", "CAndlestick", ["trade", "depth5"]]
    invalid = ["caandlestick", 5]

    for v in valid:
        options.datasources = v
        if type(v) is str:
            vl = v.lower()
            assert options._datasources == {vl}
        if type(v) is list:
            assert options._datasources == set(v)

    for v in invalid:
        with pytest.raises(Exception):
            options.datasources = v
