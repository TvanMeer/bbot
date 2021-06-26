import pytest

from bbot.options import Options


@pytest.fixture
def options():
    # Default demo options.
    return Options()


def test_verify_clean_mode(options):
    assert options._verify_clean_mode("DEBUG") == "DEBUG"
    assert options._verify_clean_mode("HISTORY") == "HISTORY"
    assert options._verify_clean_mode("STREAM") == "STREAM"
    assert options._verify_clean_mode("PAPER") == "PAPER"
    assert options._verify_clean_mode("TESTNET") == "TESTNET"
    assert options._verify_clean_mode("TRADE") == "TRADE"
    with pytest.raises(Exception):
        options._verify_clean_mode("foo")
    assert options._verify_clean_mode("DeBuG") == "DEBUG"


def test_verify_clean_base_assets(options):
    assert options._verify_clean_base_assets("BTC") == frozenset(
        [
            "BTC",
        ]
    )
    assert options._verify_clean_base_assets("*") == frozenset(
        [
            "*",
        ]
    )
    with pytest.raises(Exception):
        options._verify_clean_base_assets("BvghvhgvghvhvC")
    with pytest.raises(Exception):
        options._verify_clean_base_assets("BT123C")

    assert options._verify_clean_base_assets(["BTC", "ADA"]) == frozenset(["BTC", "ADA"])
    assert options._verify_clean_base_assets(["Btc", "ada"]) == frozenset(["BTC", "ADA"])
    with pytest.raises(Exception):
        options._verify_clean_base_assets(["BT123C", "ADA"])
    with pytest.raises(Exception):
        options._verify_clean_base_assets(["BTgchgghchcC", "ADA"])


def test_verify_clean_windows(options):
    assert options._verify_clean_windows({"1m": 500, "15m": 200}) == {"1m": 500, "15m": 200}
    with pytest.raises(Exception):
        options._verify_clean_windows({"2m": 500, "15m": 200})
    with pytest.raises(Exception):
        options._verify_clean_windows({"1m": 502, "15m": 200})
    with pytest.raises(Exception):
        options._verify_clean_windows(["2m", 500, "15m", 200])
    with pytest.raises(Exception):
        options._verify_clean_windows({"2m", 500, "15m", 3})


def test_getters(options):
    assert options._api_key == " "
    assert options._api_secret == " "
    assert options.mode == "DEBUG"
    assert options.base_assets == frozenset(
        [
            "BTC",
        ]
    )
    assert options.quote_assets == frozenset(
        [
            "USDT",
        ]
    )
    assert options.windows == {"1m": 500, "15m": 200}
    assert options.possible_intervals == {
        "2s": 2000,
        "1m": 60000,
        "3m": 180000,
        "5m": 300000,
        "15m": 900000,
        "30m": 1800000,
        "1h": 3600000,
        "2h": 7200000,
        "4h": 14400000,
        "6h": 21600000,
        "8h": 28800000,
        "12h": 43200000,
        "1d": 86400000,
        "3d": 259200000,
        "1w": 604800000,
    }
    assert options.possible_modes == frozenset(
        ["DEBUG", "HISTORY", "STREAM", "PAPER", "TESTNET", "TRADE"]
    )


def test_setters(options):
    options.mode = "PAPER"
    assert options.mode == "PAPER"
    options.base_assets = "XRP"
    assert options.base_assets == frozenset(
        [
            "XRP",
        ]
    )
    options.quote_assets = "USDC"
    assert options.quote_assets == frozenset(
        [
            "USDC",
        ]
    )
    options.windows = {"1h": 300}
    assert options.windows == {"1h": 300}
