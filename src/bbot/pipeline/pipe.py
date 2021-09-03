# pylint: disable=no-name-in-module

from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime
from enum import Enum
from typing import Any, List, Tuple

from models.candle import Candle
from models.database import ContentType, DataBase, Window
from models.options import Options
from models.timeframe import TimeFrame


class PayloadBelongsToTimeframe(str, Enum):
        CURRENT:  "CURRENT"
        PREVIOUS: "PREVIOUS"
        NEXT:     "NEXT"
        FIRST:    "FIRST"

class Pipeline(ABC):
    """Handles insertion of content in the database."""

    
    n_items_processed = Counter(
        {
            ContentType.CANDLE_HISTORY: 0,
            ContentType.CANDLE_STREAM:  0,
        }
    )


    def process(
        self, 
        symbol:      str, 
        interval:    Options.Interval, 
        contenttype: ContentType, 
        payload:     Any, 
        db:          DataBase
    ) -> DataBase:
        """Calls process_window() for the windows that should be updated."""

        self.n_items_processed.update(contenttype)

        def one_window(self):
            db.symbols[symbol].windows[interval] = self.process_window(
                contenttype, payload, db.symbols[symbol].windows[interval]
            )

        def all_windows(self):
            for iv, w in db.symbols[symbol].windows.items():
                db.symbols[symbol].windows[iv] = self.process_window(contenttype, payload, w)

        apply_on_n_windows = {
            ContentType.CANDLE_HISTORY: one_window,
            ContentType.CANDLE_STREAM:  all_windows,
        }
        apply_on_n_windows[contenttype].__call__(self)
        return db



    def process_window(
        self, 
        contenttype: ContentType, 
        payload:     Any, 
        window:      Window
    ) -> Window:
        """Interface for all pipelines. Payload is inserted in window and window is returned."""

        if not window._history_downloaded and not contenttype == ContentType.CANDLE_HISTORY:
            pass

        o, c = self.get_open_close_time(payload)
        p    = self.in_timeframe(c, window)

        if   p == PayloadBelongsToTimeframe.CURRENT:
            window = self.update_timeframe(payload, window)

        elif p == PayloadBelongsToTimeframe.PREVIOUS:
            window = self.update_timeframe(payload, window, prev_timeframe=True)

        elif p == PayloadBelongsToTimeframe.NEXT:
            window = self.create_next_timeframe(window)
            window = self.insert_in_next_timeframe(payload, window)

        elif p == PayloadBelongsToTimeframe.FIRST:
            if o:
                window = self.create_first_timeframe(o, c, window)
                window = self.insert_first_time(payload, window)
            else:
                # No open time given, drop payload and return unmodified window
                return window
        else:
            raise Exception("Could not determine in which timeframe payload belongs.")

        return window

    

    def in_timeframe(self, close_time, window) -> str:
        """Returns what timeframe the item belongs to."""

        if not window.timeframes:
            return PayloadBelongsToTimeframe.FIRST

        tf = window.timeframes[-1]
        delta = tf.close_time - tf.open_time

        if close_time > tf.close_time + delta:
            raise Exception("Error in timeframe creation.")

        elif close_time > tf.close_time:
            return PayloadBelongsToTimeframe.NEXT

        elif close_time > tf.open_time:
            return PayloadBelongsToTimeframe.CURRENT

        elif close_time > tf.open_time - delta:
            return PayloadBelongsToTimeframe.PREVIOUS
        else:
            raise Exception("Data leakage: data in pipeline lags behind.")
  


    def create_first_timeframe(self, open_time, close_time, window) -> Window:
        new_timeframe = TimeFrame(
            open_time=open_time, close_time=close_time
        )
        return window.timeframes.append(new_timeframe)


    def create_next_timeframe(self, window) -> Window:
        last = window.timeframes[-1]
        new_timeframe = TimeFrame.create_next_timeframe(
                last.open_time, last.close_time
        )
        return window.timeframes.append(new_timeframe)



    @abstractmethod
    def get_open_close_time(self, payload: Any) -> Tuple[datetime, datetime]:
        """Parse and return both open en close time in payload.
        Returns two datetime objects, or (None, <datatime>) when no open-time
        is available, like in realtime trade updates.
        """

        pass


    @abstractmethod
    def insert_first_time(self, payload: Any, window: Window) -> Window:
        """Insert payload in timeframe when timeframe is empty. E.g. a new
        candle in a timeframe where timeframe.candle == None.
        This function requires a window instead of a timeframe, to access
        metadata in its corresponding window.
        """

        pass

    @abstractmethod
    def insert_in_next_timeframe(self, payload: Any, window: Window) -> Window:
        """Insert payload in next timeframe in the sequence of timeframes."""

        pass


    @abstractmethod
    def update_timeframe(self, payload: Any, window: Window, prev_timeframe = False) -> Window:
        """Update the current, or previous timeframe."""

        pass



class HistoricalCandlePipe(Pipeline):

    def get_open_close_time(self, payload: List) -> Tuple[datetime, datetime]:
        o = datetime(payload[0])
        c = datetime(payload[6])
        return (o, c)


    def insert_first_time(self, payload: List, window: Window) -> Window:
        candle = Candle.parse_historical_candle(payload)
        window.timeframes[-1].candle = candle
        return window


    def insert_in_next_timeframe(self, payload: List, window: Window) -> Window:
        generated_tf = window.timeframes[-1]
        o, c = self.get_open_close_time(payload)
        if generated_tf.open_time != o or generated_tf.close_time != c:
            raise Exception("Inconsistent open and close times in historical candle data.")

        candle = Candle.parse_historical_candle(payload)
        window.timeframes[-1].candle = candle
        return window


    def update_timeframe(self, payload: Any, window: Window, prev_timeframe: bool) -> Window:
        raise Exception("Trying to update timeframe in historical data.")



class StreamCandlePipe(Pipeline):

    def get_open_close_time(self, payload: dict) -> Tuple[datetime, datetime]:
        pass

    def insert_first_time(self, payload: dict, window: Window) -> Window:
        pass

    def insert_in_next_timeframe(self, payload: dict, window: Window) -> Window:
        pass

    def update_timeframe(self, payload: dict, window: Window, prev_timeframe: bool) -> Window:
        pass
        