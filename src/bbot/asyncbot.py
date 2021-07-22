import asyncio


class _AsyncBot:
    """Holds internal implementation of bot. Can run in separate process of thread."""

    def __init__(self, options):
        self.options = options
        self.candles = {}
        self.user_events = []
        self.q = asyncio.Queue()

    def download_all_symbols(self, options):
        pass

    def select_symbols(self, all_symbols, options):
        pass

    def download_exchange_info(self):
        pass

    def download_account_info(self):
        pass

    def start_loops(self):
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
