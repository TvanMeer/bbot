import asyncio
from binance import AsyncClient, BinanceSocketManager
from pydantic import BaseModel
from pydantic.types import PositiveInt, condecimal

from .database import ContentType
from .options import Options


class Candle(BaseModel):
    """Candlestick from websocket stream.

    {
      "e": "kline",     // Event type
      "E": 123456789,   // Event time
      "s": "BNBBTC",    // Symbol
      "k": {
        "t": 123400000, // Kline start time
        "T": 123460000, // Kline close time
        "s": "BNBBTC",  // Symbol
        "i": "1m",      // Interval
        "f": 100,       // First trade ID
        "L": 200,       // Last trade ID
        "o": "0.0010",  // Open price
        "c": "0.0020",  // Close price
        "h": "0.0025",  // High price
        "l": "0.0015",  // Low price
        "v": "1000",    // Base asset volume
        "n": 100,       // Number of trades
        "x": false,     // Is this kline closed?
        "q": "1.0000",  // Quote asset volume
        "V": "500",     // Taker buy base asset volume
        "Q": "0.500",   // Taker buy quote asset volume
        "B": "123456"   // Ignore
      }
    }

    """

    open_price:         condecimal(decimal_places=8, gt=0)  # o
    close_price:        condecimal(decimal_places=8, gt=0)  # c
    high_price:         condecimal(decimal_places=8, gt=0)  # h
    low_price:          condecimal(decimal_places=8, gt=0)  # l
    base_volume:        condecimal(decimal_places=8)        # v
    quote_volume:       condecimal(decimal_places=8)        # q
    base_volume_taker:  condecimal(decimal_places=8)        # V
    quote_volume_taker: condecimal(decimal_places=8)        # Q
    n_trades:           PositiveInt                         # n



    @classmethod
    async def stream_coro(
        cls,
        symbol:        str,
        queue:         asyncio.Queue,
        manager:       BinanceSocketManager,
        shutdown_flag: bool,
    ) -> None:
        """Coroutine that streams candle data for a single symbol through a websocket.

        Single candles are added to the queue, as tuple(symbol, interval, content_type, raw_candle)
        Streams are always 1 minute candles. Windows are programatically updated later.
        This way bbot requires only one stream for multiple windows.
        """

        socket = manager.kline_socket(symbol)
        async with socket as candle_socket:
            while not shutdown_flag:
                raw_candle = await candle_socket.recv()
                msg = (symbol, "*", ContentType.candle_stream, raw_candle)
                await queue.put(msg)



    @classmethod
    async def history_coro(
        cls,
        symbols:       set[str],
        intervals:     set[Options.Interval],
        window_length: int,
        queue:         asyncio.Queue,
        client:        AsyncClient,
        shutdown_flag: bool,
    ) -> None:
        """Coroutine that downloads historical candle data for all selected symbols and time intervals.

        Single candles are added to the queue, as tuple(symbol, interval, content_type, raw_candle)
        After n candles are processed, where n == window_length, a `finish` notification is added to the queue.
        After every filled window, the coroutine pauzes for 5 seconds, to avoid API abuse.
        This procedure can be cancelled by setting `shutdown_flag` to true.
        """

        def gen_timestring(i, l):
            amount = i[:-1]
            period = i[-1]
            total  = str(l * amount)
            if period == "m":
                return total + " minutes ago UTC"
            elif period == "h":
                return total + " hours ago UTC"
            elif period == "d":
                return total + " days ago UTC"
            else:
                return total + " weeks ago UTC"

        async def download_window(s, i, t):
            async for raw_candle in await client.get_historical_klines_generator(
                s.upper(), i, t
            ):
                msg = (s, Options.Interval(i), ContentType.candle_history, raw_candle)
                await queue.put(msg)

        for s in symbols:
            for i in intervals:
                symbol = s
                interval = i.value
                time = gen_timestring(interval, window_length)
                if shutdown_flag:
                    return
                elif i == Options.Interval.second_2:
                    continue
                else:
                    await download_window(symbol, interval, time)
                    await queue.put(
                        ("candle_history_finished", symbol, interval)
                    )
                    await asyncio.sleep(5)
