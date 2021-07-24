import asyncio
from binance.client import AsyncClient


class _AsyncBot:
    """Holds internal implementation of bot.
    Can run in separate process of thread.
    """

    def __init__(self, options):

        self.options = options
        self.candles = {}
        self.user_events = []

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.q = asyncio.Queue()

        self.shutdown_flag = False
        self.finished_history_download = set()

        if options.mode != "DEBUG":
            self.loop.run_until_complete(self.prepare)
            self.loop.run_until_complete(self.start_loops)

    async def prepare(self):

        self.client = await AsyncClient.create(
            api_key=self.options.api_key,
            api_secret=self.options.api_secret,
            testnet=self.options.mode == "DEBUG",
        )
        self.all_symbols = await self.download_all_symbols(self.client)
        self.selected_symbols = self.select_symbols(
            self.all_symbols, self.options
        )
        self.exchange_info = await self.download_exchange_info(self.client)
        self.account_info = await self.download_account_info(self.client)

    async def download_all_symbols(self, client):
        tickers = await client.get_all_tickers()
        all_symbols = set()
        [all_symbols.add(t["symbol"]) for t in tickers]
        return all_symbols

    def select_symbols(self, all_symbols, options):

        selected = set()

        def exact_match(b, q):

            if "*" not in [b, q]:
                left = s[: len(b)]
                right = s[len(b) :]
                if left == b and right == q:
                    selected.add(s)
            else:
                selected.add(s)

        for s in all_symbols:
            for b in options.base_assets:
                if s.startswith(b) or b == "*":
                    for q in options.quote_assets:
                        if s.endswith(q) or q == "*":
                            exact_match(b, q)

        return selected

    async def download_exchange_info(self, client):

        info = await client.get_exchange_info()
        return info

    async def download_account_info(self, client):

        info = await client.get_account()
        return info

    async def start_loops(self):
        pass

    async def public_interface_listener(self):
        pass

    async def history_downloader(self):
        pass

    async def candle_streamer(self):
        pass

    async def user_event_listener(self):
        pass

    async def consumer(self):
        pass

    async def log_raw_data(self, event):
        pass

    def dispatch_event(self, event):
        pass

    def handle_public_request(self, public_interface_request):
        pass

    def handle_candle(self, candle):
        pass

    def handle_user_event(self, user_event):
        pass
