"""

Main

"""
import time

import threading
import asyncio
from binance import AsyncClient, BinanceSocketManager

from options import Options
from pair import Pair

class Bot():

    
    def __init__(self, options, api_key=' ', api_secret=' '):
        
        self.symbols       = set()
        self.pairs         = {}
        self._options      = options
        self.__api_key     = api_key
        self.__api_secret  = api_secret
        self._shutdown     = False
        self._all_symbols  = set()
        self._chanels      = []

        if options.mode in ['TESTNET', 'TRADE']:
            if api_key == ' ' or api_secret == ' ':
                raise Exception(f'Binance API credentials required in {options.mode} mode')

        # Start client in another thread
        self._binance_client = threading.Thread(target = self._other_thread, daemon=True)
        self._binance_client.start()
    

    def _other_thread(self):

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._start_async_client())


    async def _start_async_client(self):

        # Connect to Binance
        client  = await AsyncClient.create(api_key = self.__api_key, 
                                           api_secret = self.__api_secret)
        
        # Pick pairs of interest
        tickers = await client.get_all_tickers()
        [self._all_symbols.add(s['symbol']) for s in tickers]
        for qa in self._options.quote_assets:
            for s in self._all_symbols:
                if s.endswith(qa):
                    starts_with = s[:-len(qa)]
                    if starts_with in self._options.base_assets:
                        self.symbols.add(s)
                        self._chanels.append(s.lower() + '@kline_1m')

        # Initialize self.pairs
        for s in self.symbols:
            self.pairs[s] = Pair(s, self._options)

        # Concurrent execution of history download and streams
        __hist = asyncio.create_task(self._download_history(client))
        __cs   = asyncio.create_task(self._start_candle_streams(client))
        await __cs, __hist


    async def _download_history(self, client):
        for s in self.symbols:
            for w in self._options.windows.items():
                if w[0] == '2s' or w[0] == '30s':
                    continue
                timestr = self._to_timestring(w[0], w[1])
                candles = await client.get_historical_klines(s, w[0], timestr)
                self.pairs[s]._add_historical_window(w[0], candles)


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
        ms = bm.multiplex_socket(self._chanels)
        async with ms as stream:
            while self._shutdown == False:
                msg = await stream.recv()
                symbol = msg['data']['s']
                self.pairs[symbol]._parse_candle(msg)

        await client.close_connection()

    
    def stop(self):
        self._shutdown = True
        self._binance_client.join()

        




# test ------------------------------------------------------
if __name__ == '__main__':

    options = Options(mode     = 'PAPER',
                  base_assets  = [ 'BTC', 'ETH' ],
                  quote_assets = [ 'USDT', ],
                  windows      = { '1m':500, '15m':200 }
                  )

    bot    = Bot(options)
    
    
    
    time.sleep(3)
    print('Slept 3 seconds...')
    time.sleep(6)
    print('Slept 6 seconds...')

    # Test stop function
    bot.stop()

    print('Runs succesfully after termination..............')

    # TODO: model training func as param in options.
    # This is being executed as asyncio.as_thread in hist and stream
    # gather

    # Trick with shutdown also works for other functions nested within
    # candlestream while-loop
