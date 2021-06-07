"""

Main

"""
import threading
import asyncio
from binance import AsyncClient, BinanceSocketManager

from options import Options
from pair import Pair

class Bot():

    
    def __init__(self, options, api_key=' ', api_secret=' '):
        
        self.__options      = options
        self.__api_key      = api_key
        self.__api_secret   = api_secret
        self.__all_symbols  = set()
        self.__chanels      = []
        self.symbols = set()
        self.pairs   = {}

        if options.mode in ['TESTNET', 'TRADE']:
            if api_key == ' ' or api_secret == ' ':
                raise Exception(f'Binance API credentials required in {options.mode} mode')

        # Start client in another thread
        loop = asyncio.get_event_loop()
        self.binance_client = threading.Thread(target = self._other_thread, 
                                               args = (loop,)
                                               )
        self.binance_client.start()
        self.binance_client.join()


    def _other_thread(self, loop):
        try:
            loop.run_until_complete(self._start_async_client())
        finally:
            loop.close()

    async def _start_async_client(self):

        # Connect to Binance
        client  = await AsyncClient.create(api_key=self.__api_key, 
                                           api_secret=self.__api_secret)
        
        # Pick pairs of interest
        tickers = await client.get_all_tickers()
        [self.__all_symbols.add(s['symbol']) for s in tickers]
        for qa in self.__options.quote_assets:
            for s in self.__all_symbols:
                if s.endswith(qa):
                    starts_with = s[:-len(qa)]
                    if starts_with in self.__options.base_assets:
                        self.symbols.add(s)
                        self.__chanels.append(s.lower() + '@kline_1m')

        # Initialize self.pairs
        for s in self.symbols:
            self.pairs[s] = Pair(s)

        # Concurrent execution of history download and streams
        __hist = asyncio.create_task(self._download_history(client))
        __cs   = asyncio.create_task(self._start_candle_streams(client))
        _      = await asyncio.gather(__hist, __cs)

        await client.close_connection()


    async def _download_history(self, client):
        for s in self.symbols:
            for w in self.__options.windows.items():
                if w[0] == '2s':
                    continue
                timestr = self._to_timestring(w[0], w[1])
                candles = await client.get_historical_klines(s, w[0], timestr)
                self.pairs[s].add_historical_window(w[0], candles)


    def _to_timestring(self, interval, windowsize):
        # Helperfunction to download history with binance-python
        amount = int(interval[:-1]) * windowsize
        period = interval[-1]
        if period == 'm':
            return f'{amount} minutes ago UTC'
        elif period == 'h':
            return f'{amount} hours ago UTC'
        elif period == 'd':
            return f'{amount} days ago UTC'
        elif period == 'w':
            return f'{amount} weeks ago UTC'
        elif period == 'M':
            return f'{amount} months ago UTC'
        else:
            raise Exception(f'Error: invalid interval:  {period}')

    
    async def _start_candle_streams(self, client):
        bm = BinanceSocketManager(client)
        ms = bm.multiplex_socket(self.__chanels)
        async with ms as stream:
            while True:
                msg = await stream.recv()
                symbol = msg['data']['s']
                self.pairs[symbol].add_candle(msg)



# test ------------------------------------------------------
if __name__ == '__main__':

    options = Options(mode     = 'PAPER',
                  base_assets  = [ 'BTC', 'ETH' ],
                  quote_assets = [ 'USDT', ],
                  windows      = { '1m':500, '15m':200 }
                  )

    bot    = Bot(options)
