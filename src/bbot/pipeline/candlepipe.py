from typing import List, Tuple

from .pipe import Pipeline
from models.database import DataBase, Window
from models.candle import Candle
from models.options import Options



class CandleHistoryPipeline(Pipeline):

    def get_window(self, raw: Tuple[str, Options.Interval, List], db: DataBase) -> Window:
        """Receives a tuple (symbol, interval, raw_candle).
        Only returns the corresponding window in the database.
        """

        pass

    def parse(self, raw: List) -> Candle:
        """Turns historical candle into a Candle object."""

        pass

    def insert(self, candle: Candle, window: Window) -> DataBase:
        """Inserts the historical candle in the corresponding window.
        Then inserts the window in the database and returns the updated database.
        """

        pass



class CandlePipeline(Pipeline):

    def get_window(self, raw: dict, db: DataBase) -> Window:
        """Receives a candle as a dictionary from a websocket.
        Finds and returns the corresponding window in the database.
        """

        pass

    def parse(self, raw: dict) -> Candle:
        """Turns latest candle from websocket into a Candle object."""

        pass

    def insert(self, candle: Candle, window: Window) -> DataBase:
        """Inserts the new candle in the corresponding window.
        Then inserts this window in the database and returns the updated database.
        """

        pass