import asyncio
from binance.client import AsyncClient


class _AsyncBot:
    """Holds internal implementation of bot.
    Can run in separate process or thread.
    """

    def __init__(self, options):

        self.options = options

        t = lambda coro: asyncio.create_task(coro)

        t1 = t(self.prepare_connection)
        t2 = t(self.prepare_database)
        t3 = t(self.download_history)

        # Infinite loops
        t4 = t(self.consumer)
        t5 = t(self.candle_producer)
        t6 = t(self.miniticker_producer)
        t7 = t(self.ticker_producer)
        t8 = t(self.depth_producer)
        t9 = t(self.userevent_producer)

        mode_filter = {
            "test":    None,
            "debug":   {t1, t2},
            "history": {t1, t2},
            "stream":  {t1, t2, t4},
            "paper":   {t1, t2, t4, t9},
            "trade":   {t1, t2, t4, t9},
        }
        streams_filter = {
            "candle":     {t3, t4, t5}, 
            "miniticker": {t4, t6},
            "ticker":     {t4, t7},
            "depth5":     {t4, t8},
            "depth10":    {t4, t8},
            "depth20":    {t4, t8},
        }

        selected_mode = mode_filter[options.mode]
        selected_streams = set()
        [selected_streams.add(streams_filter[s]) for s in options.streams]
        selected_tasks = selected_mode.union(selected_streams)
        

        # Shared variables
        self.client = None
        self.database = None
        self.queue = asyncio.Queue()

        # State variables
        self.t1_complete = False
        self.t2_complete = False
        self.t3_complete = False

        if selected_tasks is not None:
            asyncio.gather(*selected_tasks)


    async def prepare_connection(self):
        pass

    async def prepare_database(self):
        while not self.t1_complete:
            asyncio.sleep(0.1)

    async def download_history(self):
        while not self.t2_complete:
            asyncio.sleep(0.1)
        if "candle" in self.options.streams:
            pass


    # Infinite loops --------------------------------------------------------

    async def consumer(self):
        pass

    async def candle_producer(self):
        while not self.t3_complete:
            asyncio.sleep(0.01)

    async def miniticker_producer(self):
        while not self.t3_complete:
            asyncio.sleep(0.01)

    async def ticker_producer(self):
        while not self.t3_complete:
            asyncio.sleep(0.01)

    async def depth_producer(self):
        while not self.t3_complete:
            asyncio.sleep(0.01)

    async def userevent_producer(self):
        pass
