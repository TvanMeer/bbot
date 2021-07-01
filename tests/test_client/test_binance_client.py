from binance import AsyncClient
import asyncio
import pytest

from bbot.options import Options

# Raw data as provided by python-binance -----------------------------------------------------


@pytest.fixture
def all_tickers():
    return [
        {"symbol": "BTCUSDT", "price": "0.22540000"},
        {"symbol": "ADAUSDT", "price": "0.02093000"},
        {"symbol": "BTCUSDC", "price": "0.70170000"},
        {"symbol": "XRPBTC", "price": "12345.74780000"},
        {"symbol": "BTCxxxxxUSDT", "price": "34437.11000000"},
    ]


# 2 minute candles
@pytest.fixture
def history_1m():
    return [
        [
            1624934520000,
            "34406.08000000",
            "34437.11000000",
            "34395.07000000",
            "34431.47000000",
            "18.20600800",
            1624934579999,
            "626663.26924604",
            560,
            "10.84483500",
            "373333.75765970",
            "0",
        ],
        [
            1624934580000,
            "34431.47000000",
            "34440.86000000",
            "34431.47000000",
            "34438.75000000",
            "1.56972700",
            1624934639999,
            "54055.33589430",
            61,
            "1.32232600",
            "45535.39363053",
            "0",
        ],
    ]


# 2 weekly candles
@pytest.fixture
def history_1w():
    return [
        [
            1624233600000,
            "35600.17000000",
            "35750.00000000",
            "28805.00000000",
            "34700.34000000",
            "907073.70759800",
            1624838399999,
            "29582225083.09103260",
            15069286,
            "445188.23814000",
            "14532263176.09752217",
            "0",
        ],
        [
            1624838400000,
            "34702.49000000",
            "35297.71000000",
            "33862.72000000",
            "34388.92000000",
            "90903.89463600",
            1625443199999,
            "3138756013.48975434",
            2044510,
            "45108.65752200",
            "1558236653.33225741",
            "0",
        ],
    ]


@pytest.fixture
def historical_candle():
    return [
        1624934520000,
        "34406.08000000",
        "34437.11000000",
        "34395.07000000",
        "34431.47000000",
        "18.20600800",
        1624934579999,
        "626663.26924604",
        560,
        "10.84483500",
        "373333.75765970",
        "0",
    ]


@pytest.fixture
def candle():
    return {
        "stream": "btcusdt@kline_1m",
        "data": {
            "e": "kline",
            "E": 1624935608626,
            "s": "BTCUSDT",
            "k": {
                "t": 1624935600000,
                "T": 1624935659999,
                "s": "BTCUSDT",
                "i": "1m",
                "f": 937706327,
                "L": 937706450,
                "o": "34312.62000000",
                "c": "34315.07000000",
                "h": "34315.36000000",
                "l": "34307.15000000",
                "v": "4.66117500",
                "n": 124,
                "x": False,
                "q": "159923.57796175",
                "V": "1.72322000",
                "Q": "59122.29261096",
                "B": "0",
            },
        },
    }


@pytest.fixture
def candles():
    return {
        "stream": "xrpusdt@kline_1m",
        "data": {
            "e": "kline",
            "E": 1624935605165,
            "s": "XRPUSDT",
            "k": {
                "t": 1624935600000,
                "T": 1624935659999,
                "s": "XRPUSDT",
                "i": "1m",
                "f": 287563962,
                "L": 287564000,
                "o": "0.64670000",
                "c": "0.64640000",
                "h": "0.64670000",
                "l": "0.64630000",
                "v": "69679.44000000",
                "n": 39,
                "x": False,
                "q": "45051.82443200",
                "V": "5182.50000000",
                "Q": "3351.06085300",
                "B": "0",
            },
        },
    }


{
    "stream": "btcusdt@kline_1m",
    "data": {
        "e": "kline",
        "E": 1624935606312,
        "s": "BTCUSDT",
        "k": {
            "t": 1624935600000,
            "T": 1624935659999,
            "s": "BTCUSDT",
            "i": "1m",
            "f": 937706327,
            "L": 937706427,
            "o": "34312.62000000",
            "c": "34312.31000000",
            "h": "34312.62000000",
            "l": "34307.15000000",
            "v": "4.26575100",
            "n": 101,
            "x": False,
            "q": "146354.88983529",
            "V": "1.45822100",
            "Q": "50029.06152155",
            "B": "0",
        },
    },
}
{
    "stream": "xrpusdt@kline_1m",
    "data": {
        "e": "kline",
        "E": 1624935608175,
        "s": "XRPUSDT",
        "k": {
            "t": 1624935600000,
            "T": 1624935659999,
            "s": "XRPUSDT",
            "i": "1m",
            "f": 287563962,
            "L": 287564003,
            "o": "0.64670000",
            "c": "0.64650000",
            "h": "0.64670000",
            "l": "0.64630000",
            "v": "70801.49000000",
            "n": 42,
            "x": False,
            "q": "45777.13794000",
            "V": "6304.55000000",
            "Q": "4076.37436100",
            "B": "0",
        },
    },
}
{
    "stream": "btcusdt@kline_1m",
    "data": {
        "e": "kline",
        "E": 1624935608626,
        "s": "BTCUSDT",
        "k": {
            "t": 1624935600000,
            "T": 1624935659999,
            "s": "BTCUSDT",
            "i": "1m",
            "f": 937706327,
            "L": 937706450,
            "o": "34312.62000000",
            "c": "34315.07000000",
            "h": "34315.36000000",
            "l": "34307.15000000",
            "v": "4.66117500",
            "n": 124,
            "x": False,
            "q": "159923.57796175",
            "V": "1.72322000",
            "Q": "59122.29261096",
            "B": "0",
        },
    },
}


@pytest.fixture
def user_event_account_update():
    return {
        "e": "outboundAccountPosition",  # Event type
        "E": 1564034571105,  # Event Time
        "u": 1564034571073,  # Time of last account update
        "B": [  # Balances Array
            {
                "a": "ETH",  # Asset
                "f": "10000.000000",  # Free
                "l": "0.000000",  # Locked
            }
        ],
    }


@pytest.fixture
def user_event_balance_update():
    return {
        "e": "balanceUpdate",  # Event Type
        "E": 1573200697110,  # Event Time
        "a": "BTC",  # Asset
        "d": "100.00000000",  # Balance Delta
        "T": 1573200697068,  # Clear Time
    }


@pytest.fixture
def user_event_order_update_execution_report():
    return {
        "e": "executionReport",  # Event type
        "E": 1499405658658,  # Event time
        "s": "ETHBTC",  # Symbol
        "c": "mUvoqJxFIILMdfAW5iGSOW",  # Client order ID
        "S": "BUY",  # Side
        "o": "LIMIT",  # Order type
        "f": "GTC",  # Time in force
        "q": "1.00000000",  # Order quantity
        "p": "0.10264410",  # Order price
        "P": "0.00000000",  # Stop price
        "F": "0.00000000",  # Iceberg quantity
        "g": -1,  # OrderListId
        "C": "",  # Original client order ID; This is the ID of the order being canceled
        "x": "NEW",  # Current execution type
        "X": "NEW",  # Current order status
        "r": "NONE",  # Order reject reason; will be an error code.
        "i": 4293153,  # Order ID
        "l": "0.00000000",  # Last executed quantity
        "z": "0.00000000",  # Cumulative filled quantity
        "L": "0.00000000",  # Last executed price
        "n": "0",  # Commission amount
        "N": None,  # Commission asset
        "T": 1499405658657,  # Transaction time
        "t": -1,  # Trade ID
        "I": 8641984,  # Ignore
        "w": True,  # Is the order on the book?
        "m": False,  # Is this trade the maker side?
        "M": False,  # Ignore
        "O": 1499405658657,  # Order creation time
        "Z": "0.00000000",  # Cumulative quote asset transacted quantity
        "Y": "0.00000000",  # Last quote asset transacted quantity (i.e. lastPrice * lastQty)
        "Q": "0.00000000",  # Quote Order Qty
    }


@pytest.fixture
def user_event_order_update_list_status():
    return {
        "e": "listStatus",  # Event Type
        "E": 1564035303637,  # Event Time
        "s": "ETHBTC",  # Symbol
        "g": 2,  # OrderListId
        "c": "OCO",  # Contingency Type
        "l": "EXEC_STARTED",  # List Status Type
        "L": "EXECUTING",  # List Order Status
        "r": "NONE",  # List Reject Reason
        "C": "F4QN4G8DlFATFlIUQ0cjdD",  # List Client Order ID
        "T": 1564035303625,  # Transaction Time
        "O": [  # An array of objects
            {
                "s": "ETHBTC",  # Symbol
                "i": 17,  # orderId
                "c": "AJYsMjErWJesZvqlJCTUgL",  # ClientOrderId
            },
            {"s": "ETHBTC", "i": 18, "c": "bfYPSQdLoqAJeNrOr9adzq"},
        ],
    }


# Other fixtures --------------------------------------------------------


@pytest.fixture
def options():
    return Options()


@pytest.fixture
@pytest.mark.asyncio
async def async_client(options):
    return await AsyncClient.create(
        api_key=options._api_key, api_secret=options._api_secret
    )


@pytest.fixture
def all_symbols():
    return frozenset(
        ["BTCUSDT", "ADAUSDT", "BTCUSDC", "XRPBTC", "BTCxxxxxUSDT"]
    )


@pytest.fixture
def selected_symbols():
    return frozenset(
        [
            "BTCUSDT",
        ]
    )


@pytest.fixture
def window_options():
    return Options().windows

@pytest.fixture
def parsed_historical_candle():
    pass #TODO

@pytest.fixture
def parsed_new_candle():
    pass #TODO


# Unit tests ------------------------------------------------------------
def test_init(options):
    pass


@pytest.mark.asyncio
async def test_create_async_client(options):
    pass


@pytest.mark.asyncio
async def test_download_all_symbols(async_client):
    pass


def test_parse_all_symbols(all_tickers):
    pass


@pytest.mark.asyncio
async def test_download_history(
    selected_symbols, window_options, async_client
):
    pass


def test_parse_historical_candle(historical_candle):
    pass


@pytest.mark.asyncio
async def test_start_candle_sockets(selected_symbols, async_client):
    pass


def test_parse_new_candle(candle):
    pass


@pytest.mark.asyncio
async def test_start_user_socket(async_client):
    pass


def test_parse_user_event_account_update(user_event_account_update):
    pass


def test_parse_user_event_balance_update(user_event_balance_update):
    pass


def test_parse_user_event_order_update_execution_report(
    user_event_order_update_execution_report,
):
    pass


def test_parse_user_event_order_update_list_status(
    user_event_order_update_list_status,
):
    pass
