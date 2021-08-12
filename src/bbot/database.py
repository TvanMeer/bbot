class Database:
    def __init__(self, options):
        self.OPTIONS = options
        self.ALL_SYMBOLS = None
        self.SELECTED_SYMBOLS = None

        self.exchange_info = None
        self.account_info = None
        self._realtime_data = None
        self.coininfo = None
        self.user_events = []

        # State variables
        self._current_event_time_open = int
        self._current_event_time_close = int
        self._history_download_finished_symbols = set()

    # Internal
    def _init_timeframes(self, selected_symbols):
        tf = {}
        for sym in selected_symbols:
            tf[sym] = {}
            for interval in self.OPTIONS.windows.keys():
                tf[sym][interval] = []
        self._realtime_data = tf

    def _init_coininfo(self, selected_symbols):
        for s in selected_symbols:
            self.coininfo[s] = {}

    # Public
    @property    #TODO: coininfo also in _realtime_data
    def get(self):
        """
        Gets dict with all windows for all selected symbols.
        Should be used in combination with a selector like this:
        db.get["btcusdt"]["1m"]

        Returns self.timeframes, in this format:

        {
            "btcusdt": {
                "1m" : [<timeframe>],
                "15m": [<timeframe>]
            }
            "hotusdt": {
                "1m" : [<timeframe>],
                "15m": [<timeframe>]
            }
        }


        <timeframe> has got the following format:

        {
            # candlestick                             # Candle socket

            "time_open"         : 123400000,          # Kline start time
            "time_close"        : 123460000,          # Kline close time
            "open_price"        : 0.0010,             # Open price
            "close_price"       : 0.0020,             # Close price
            "high_price"        : 0.0025,             # High price
            "low_price"         : 0.0015,             # Low price
            "base_volume"       : 1000,               # Base asset volume
            "quote_volume"      : 1.0000,             # Quote asset volume
            "base_volume_taker" : 500,                # Taker buy base asset volume
            "quote_volume_taker": 0.500,              # Taker buy quote asset volume
            "n_trades"          : 100,                # Number of trades

            # rolling24                               # Miniticker socket

            "open_price24"      : 0.0010,             # Open price 24 hours ago
            "high_price24"      : 0.0025,             # Highest price in the last 24 hours
            "low_price24"       : 0.0010,             # Lowest price in the last 24 hours
            "base_volume24"     : 10000,              # Base asset volume in the last 24 hours
            "quote_volume24"    : 1.0000,             # Quote asset volume in the last 24 hours

                                                      # Ticker socket

            "price_change24"    : 0.0015,             # Price change in the last 24 hours
            "price_change24_percentage" : 250.00,     # Percentage price change in the last 24 hours
            "weighted_average_price24" : 0.0018,      # Weighted average price
            "best_bid_price24"    : 0.0024,           # Best bid price in the last 24 hours
            "best_bid_quantity24" : 10,               # Best bid quantity
            "best_ask_price24": 0.0026,               # Best ask price in the last 24 hours
            "best_ask_quantity24" : 100,              # Best ask quantity
            "n_trades24" : 18151,                     # Number of trades in the last 24 hours

            # depth5

            "top5_bids" : [(price, quantity), ...],   # Depthchart at close time of timeframe.
            "top5_asks" : [[price, quantity], ...]


        }

        """
        return self._realtime_data

    