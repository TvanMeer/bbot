import asyncio
import json

from binance import AsyncClient, BinanceSocketManager


async def main():
    """This script downloads samples of all raw data consumed by Bbot."""

    async def create_auth_client():
        """Creates authenticated testnet client. Uses key and secret located in the file `credentials.json`
        in the root of the project. credentials.json lists testnet credentials and has the following format:

        {
            "key":    <key>,
            "secret": <secret>
        }
        """
        cred = None
        with open("credentials.json", "r") as authfile:
            data = authfile.read()
            cred = json.loads(data)
        client = await AsyncClient.create(
            api_key=cred["key"], api_secret=cred["secret"], testnet=True
        )
        return client

    async def create_client():
        """Creates unauthenticated client that consumes data from main net, not the testnet."""
        client = await AsyncClient.create(
            api_key=" ", api_secret=" ", testnet=False
        )
        return client

    async def to_file(name, data):
        formatted = json.dumps(data, indent=2)
        f = open("tests/raw_data/" + name + ".json", "w")
        f.write(formatted)
        f.close()
        await asyncio.sleep(0.25)

    client = await create_client()

    # general info ---------------------------------------------

    exchange_info = await client.get_exchange_info()
    await to_file("exchange_info", exchange_info)

    tickers = await client.get_all_tickers()
    await to_file("all_tickers", tickers)

    first_tickers = await client.get_orderbook_tickers()
    await to_file("all_tickers_first_orderbook_entry", first_tickers)

    h24_tickers = await client.get_ticker()
    await to_file("h24_tickers", h24_tickers)

    # coin info -----------------------------------------------

    depth = await client.get_order_book(symbol="BTCUSDT")
    await to_file("depth", depth)

    klines = await client.get_historical_klines(
        "BTCUSDT", AsyncClient.KLINE_INTERVAL_1MINUTE, "3 minutes ago UTC"
    )
    await to_file("hist_candles", klines)

    # websocket streams --------------------------------------

    symbol = "btcusdt"
    streams = [
        "kline_1m",
        "ticker",
        "miniTicker",
        "bookTicker",
        "depth",
        "trade",
        "aggTrade",
    ]

    async def stream_three(name, socket):
        responses = []
        async with socket as sock:
            while len(responses) < 3:
                res = await sock.recv()
                responses.append(res)
        await to_file(name, responses)

    bm = BinanceSocketManager(client)
    for s in streams:
        ms = bm.multiplex_socket([symbol + "@" + s])
        await stream_three(s, ms)
        await ms.__aexit__(None, None, None)

    # All market tickers stream
    ms = bm.multiplex_socket(["!ticker@arr"])
    await stream_three("all_tickers_stream", ms)
    await ms.__aexit__(None, None, None)

    mms = bm.multiplex_socket(["!miniTicker@arr"])
    await stream_three("all_minitickers_stream", mms)
    await ms.__aexit__(None, None, None)

    # Account info
    auth_client = await create_auth_client()
    account_info = await auth_client.get_account()
    await to_file("account_info", account_info)

    await client.close_connection()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
