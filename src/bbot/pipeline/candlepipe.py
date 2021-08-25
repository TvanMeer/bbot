from typing import List, Tuple
from datetime import time
from pydantic.error_wrappers import ValidationError

from .pipe import Pipeline
from .helpers import get_interval
from models.database import DataBase, Window
from models.candle import Candle
from models.timeframe import TimeFrame


class CandleHistoryPipeline(Pipeline):

    open_time = None
    close_time = None
    interval = None
    symbol = None


    def get_window(self, raw: Tuple[str, List], db: DataBase) -> Window:
        """Receives the symbol and historical candle as list.
        Finds and returns the corresponding window in the database.
        """

        self.symbol = raw[0].lower()
        self.open_time = raw[1][0]
        self.close_time = raw[1][6]
        self.interval = get_interval(self.open_time, self.close_time)
        return db.symbols[self.symbol].windows[self.interval]


    def parse(self, raw: List) -> Candle:
        """Turns historical candle into a Candle object."""

        try:
            c = Candle(
                open_price=raw[1],
                close_price=raw[4],
                high_price=raw[2],
                low_price=raw[3],
                base_volume=raw[5],
                quote_volume=raw[7],
                base_volume_taker=raw[9],
                quote_volume_taker=raw[10],
                n_trades=raw[8],
            )
        except ValidationError as e:
            raise Exception(e)
        return c


    def insert_in_window(self, candle: Candle, window: Window) -> Window:
        """Inserts the historical candle in the corresponding window.
        Then inserts the window in the database and returns the updated database.
        """

        try:
            # update timeframe
            window.timeframes[-1].candle = candle
        except ValidationError:
            # new timeframe
            try:
                tf = TimeFrame(
                    open_time=time(self.open_time),
                    close_time=time(self.close_time),
                    candle=candle,
                )
            except ValidationError as e:
                raise Exception(e)
            try:
                window.timeframes.append(tf)
            except ValidationError as e:
                raise Exception(e)
        return window

    
    def insert_in_db(self, window: Window, db: DataBase) -> DataBase:
        """Inserts updated window in database."""

        try:
            db.symbols[self.symbol].windows[self.interval] = window
        except ValidationError as e:
            raise Exception(e)
        return db




class CandlePipeline(Pipeline):
    def get_window(self, raw: dict, db: DataBase) -> Window:
        """Receives a candle as a dictionary from a websocket.
        Finds and returns the corresponding window in the database.
        """

        pass

    def parse(self, raw: dict) -> Candle:
        """Turns latest candle from websocket into a Candle object."""

        pass

    def insert_in_window(self, candle: Candle, window: Window) -> DataBase:
        """Inserts the new candle in the corresponding window.
        Then inserts this window in the database and returns the updated database.
        """

        pass

    def insert_in_db(self, window: Window, db: DataBase) -> DataBase:
        """Inserts updated window in database."""

        pass
