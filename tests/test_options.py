import pytest

from bbot.options import Interval, Mode, Options


@pytest.fixture
def interval():
    # single enum k-v
    return Interval.m1


@pytest.fixture
def mode():
    # Single enum k-v
    return Mode.DEBUG


@pytest.fixture
def options():
    # Default demo options.
    return Options()


def test__verify_clean_mode(options):
    assert options._verify_clean_mode("DEBUG") == Mode.DEBUG
    assert options._verify_clean_mode("HISTORY") == Mode.HISTORY
    assert options._verify_clean_mode("STREAM") == Mode.STREAM
    assert options._verify_clean_mode("PAPER") == Mode.PAPER
    assert options._verify_clean_mode("TESTNET") == Mode.TESTNET
    assert options._verify_clean_mode("TRADE") == Mode.TRADE
    with pytest.raises(Exception):
        options._verify_clean_mode("foo")
    assert options._verify_clean_mode("DeBuG") == Mode.DEBUG


def test__verify_clean_base_assets(options):
    pass  # TODO


def test__verify_clean_quote_assets(options):
    pass  # TODO


def test__verify_clean_windows(options):
    pass  # TODO


def test_getters(options):
    pass  # TODO


def test_setters(options):
    pass  # TODO
