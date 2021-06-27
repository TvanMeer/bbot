from .candle import Candle


class Window:
    """This class holds only candles of a specific time interval."""

    def __init__(self, interval: str, windowsize: int) -> None:

        self.interval = interval
        self.windowsize = windowsize
        self.candles = []

    def _add_historical_candle(self, candle: Candle) -> None:
        """Verifies and adds a single historical candle passed by
        Client.parse_historical_candle().
        """

        pass  # TODO

    def _add_new_candle(self, candle: Candle) -> None:
        pass  # TODO

    def _update_candle(self, candle: Candle) -> None:
        pass  # TODO
