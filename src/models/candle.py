# pylint: disable=no-name-in-module

import asyncio
import logging
from typing import List, Type, TypeVar

from binance import AsyncClient, BinanceSocketManager
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from pydantic.types import PositiveInt, condecimal

from ..bbot.constants import ContentType, Interval

_Candle = TypeVar("_Candle", bound="Candle")


class Candle(BaseModel):
    """Candlestick from websocket stream or historical API call.

    stream:

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


    history:

    [
      [
        1499040000000,      // Open time
        "0.01634790",       // Open
        "0.80000000",       // High
        "0.01575800",       // Low
        "0.01577100",       // Close
        "148976.11427815",  // Volume
        1499644799999,      // Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "17928899.62484339" // Ignore.
      ]
    ]


    """

    open_price:         condecimal(decimal_places=8, gt=0)  # o   1
    close_price:        condecimal(decimal_places=8, gt=0)  # c   4
    high_price:         condecimal(decimal_places=8, gt=0)  # h   2
    low_price:          condecimal(decimal_places=8, gt=0)  # l   3
    base_volume:        condecimal(decimal_places=8)        # v   5
    quote_volume:       condecimal(decimal_places=8)        # q   7
    base_volume_taker:  condecimal(decimal_places=8)        # V   9
    quote_volume_taker: condecimal(decimal_places=8)        # Q   10
    n_trades:           PositiveInt                         # n   8
    corrupt:            bool = False



    @staticmethod
    def parse_candle(raw_candle: dict) -> _Candle:
        """Parse websocket candlestick, return Candle instance."""

        try:
            return Candle(
                open_price         =raw_candle["o"],
                close_price        =raw_candle["c"],
                high_price         =raw_candle["h"],
                low_price          =raw_candle["l"],
                base_volume        =raw_candle["v"],
                quote_volume       =raw_candle["q"],
                base_volume_taker  =raw_candle["V"],
                quote_volume_taker =raw_candle["Q"],
                n_trades           =raw_candle["n"],
            )
        except ValidationError as e:
            logging.critical(e)



    @staticmethod
    def parse_historical_candle(raw_candle: List) -> _Candle:
        """Parse historical candlestick, return Candle instance."""

        try:
            return Candle(
                open_price         =raw_candle[1],
                close_price        =raw_candle[4],
                high_price         =raw_candle[2],
                low_price          =raw_candle[3],
                base_volume        =raw_candle[5],
                quote_volume       =raw_candle[7],
                base_volume_taker  =raw_candle[9],
                quote_volume_taker =raw_candle[10],
                n_trades           =raw_candle[8],
            )
        except ValidationError as e:
            logging.critical(e)



    @staticmethod
    def update(
        candle:                 Type[_Candle],
        update:                 Type[_Candle],
        previous_update:        Type[_Candle],
        previous_update_closed: bool,
    ) -> _Candle:
        """Updates and returns a candlestick."""

        new_candle = candle
        new_candle.close_price = update.close_price
        new_candle.high_price  = max(candle.high_price, update.high_price)
        new_candle.low_price   = min(candle.low_price, update.low_price)

        if previous_update_closed:
            new_candle.base_volume        += update.base_volume
            new_candle.quote_volume       += update.quote_volume
            new_candle.base_volume_taker  += update.base_volume_taker
            new_candle.quote_volume_taker += update.quote_volume_taker
            new_candle.n_trades           += update.n_trades
        else:
            new_candle.base_volume        += update.base_volume - previous_update.base_volume
            new_candle.quote_volume       += update.quote_volume - previous_update.quote_volume
            new_candle.base_volume_taker  += update.base_volume_taker - previous_update.base_volume_taker
            new_candle.quote_volume_taker += update.quote_volume_taker - previous_update.quote_volume_taker
            new_candle.n_trades           += update.n_trades - previous_update.n_trades

        return new_candle



    @staticmethod
    def create_2s_candle(
        update:                 Type[_Candle],
        previous_update:        Type[_Candle],
        previous_update_closed: bool,
    ) -> _Candle:
        """Produces a candle for the timeframe with an interval of 2 seconds."""

        if previous_update_closed:
          return Candle(
            open_price         = previous_update.close_price,
            close_price        = update.close_price,
            high_price         = max(update.close_price, previous_update.close_price),
            low_price          = min(update.close_price, previous_update.close_price),
            base_volume        = update.base_volume,
            quote_volume       = update.quote_volume,
            base_volume_taker  = update.base_volume_taker,
            quote_volume_taker = update.quote_volume_taker,
            n_trades           = update.n_trades
          )
        else:
          return Candle(
            open_price         = previous_update.close_price,
            close_price        = update.close_price,
            high_price         = max(update.close_price, previous_update.close_price),
            low_price          = min(update.close_price, previous_update.close_price),
            base_volume        = update.base_volume - previous_update.base_volume,
            quote_volume       = update.quote_volume - previous_update.quote_volume,
            base_volume_taker  = update.base_volume_taker - previous_update.base_volume_taker,
            quote_volume_taker = update.quote_volume_taker - previous_update.quote_volume_taker,
            n_trades           = update.n_trades - previous_update.n_trades
          )



    @staticmethod
    async def stream_producer(
        symbol:        str,
        queue:         asyncio.Queue,
        client:        AsyncClient,
        manager:       BinanceSocketManager,
        shutdown_flag: bool,
    ) -> None:
        """Coroutine that streams 1m candlestick data for a single symbol, through a websocket.

        Single candles are added to the queue, as tuple(symbol, interval, content_type, raw_candle)
        Streams are always 1 minute candles. Windows are programatically updated later.
        That way bbot requires just one stream for multiple windows.
        """

        socket = manager.kline_socket(symbol)
        async with socket as candle_socket:
            while not shutdown_flag:
                raw_candle = await candle_socket.recv()
                msg = (symbol, "*", ContentType.CANDLE_STREAM, raw_candle)
                await queue.put(msg)
        await client.close_connection()



    @staticmethod
    async def history_producer(
        symbol:        str,
        intervals:     set[Interval],
        window_length: int,
        queue:         asyncio.Queue,
        client:        AsyncClient,
        shutdown_flag: bool,
    ) -> None:
        """Coroutine that downloads historical candlestick data for a single symbol and all time intervals.

        Single candles are added to the queue, as tuple(symbol, interval, content_type, raw_candle)
        After n candles are processed, where n == window_length, a `finish` notification is added to the queue.
        After every filled window, the coroutine pauzes for 5 seconds, to avoid API abuse.
        This procedure is cancelled if `shutdown_flag` is set to true.
        """

        def gen_timestring(i, l):
            # helperfunc
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
                msg = (
                    s,
                    Interval(i),
                    ContentType.CANDLE_HISTORY,
                    raw_candle,
                )
                await queue.put(msg)

        for i in intervals:
            interval = i.value
            time = gen_timestring(interval, window_length)
            if shutdown_flag:
                return
            elif i == Interval.SECOND_2:
                continue
            else:
                await download_window(symbol, interval, time)
                await queue.put(
                  (symbol, interval, None, "finished_history_download")
                )
                await asyncio.sleep(5)

