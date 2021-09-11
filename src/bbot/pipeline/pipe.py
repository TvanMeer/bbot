# pylint: disable=no-name-in-module

from abc import ABC, abstractmethod
from collections import Counter
from datetime import datetime, timedelta
from typing import Any, List

from ..constants import ContentType, Interval, InTimeFrame
from models.candle import Candle
from models.database import DataBase
from models.timeframe import TimeFrame
from models.window import Window

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
        interval:    Interval, 
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

        apply_on_windows = {
            ContentType.CANDLE_HISTORY: one_window,
            ContentType.CANDLE_STREAM:  all_windows,
        }
        apply_on_windows[contenttype]()
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

        tf = {
            InTimeFrame.FIRST: self.first,
            InTimeFrame.PREVIOUS: self.previous,
            InTimeFrame.CURRENT: self.current,
            InTimeFrame.NEXT: self.nexxt,
            InTimeFrame.OTHER: self.data_leakage_error,
        }

        close_time = self.get_close_time(payload)
        in_tf = self.which_timeframe(close_time, window)

        return tf[in_tf](payload, window)



    def which_timeframe(self, close_time, window) -> str:
        """Returns which timeframe the item belongs to."""

        if not window.timeframes:
            return InTimeFrame.FIRST

        tf = window.timeframes[-1]
        delta = tf.close_time - tf.open_time

        if close_time > tf.close_time + delta:
            raise Exception("Error in timeframe creation.")

        if close_time > tf.close_time:
            return InTimeFrame.NEXT

        if close_time > tf.open_time:
            return InTimeFrame.CURRENT

        if close_time > tf.open_time - delta:
            return InTimeFrame.PREVIOUS

        return InTimeFrame.OTHER
  


    def data_leakage_error(self):
        e = """Data leakage: bbot cannot process the data fast enough. 
        Reduce the number of data sources or try to increase the performance
        of your feature calculation functions.
        """

        raise Exception(e)


    @abstractmethod
    def get_close_time(self, payload: Any) -> datetime:
        """Parse and return close time in payload.
        Returns datetime object.
        """

        pass


    @abstractmethod
    def first(self, payload: Any, window: Window) -> Window:
        """Inserts payload in timeframe when timeframe is empty. E.g. a new
        candle in a timeframe where timeframe.candle == None.
        This function requires a window instead of a timeframe, to access
        metadata in its corresponding window.
        """

        pass


    @abstractmethod
    def previous(self, payload: Any, window: Window) -> Window:
        """Inserts payload in previous timeframe. 
        (if the close time in payload < open time of current timeframe)
        """

        pass

    @abstractmethod
    def current(self, payload: Any, window: Window) -> Window:
        """Updates the current timeframe. (where current is window.timeframes[-1])
        """

        pass


    @abstractmethod
    def nexxt(self, payload: Any, window: Window) -> Window:
        """Creates next timeframe in window.timeframes and
        inserts payload in this new timeframe.
        """

        pass


    # Helperfuncs

    def round_time(self, close_time: datetime):
        """Rounds time to closest possible 2-second close time -1.
        Used to get 2 second candle close time based on event time.
        """
      
        return close_time - timedelta(microseconds=close_time.microsecond) - timedelta(milliseconds=1)


class HistoricalCandlePipe(Pipeline):

    def get_close_time(self, payload: List, window: Window) -> datetime:
        return datetime(payload[6])


    def first(self, payload: List, window: Window) -> Window:
        o = datetime(payload[0])
        c = datetime(payload[6])
        timeframe = TimeFrame(open_time=o, close_time=c)
        window.timeframes[0] = timeframe
        candle = Candle.parse_historical_candle(payload)
        window.timeframes[0].candle = candle
        return window


    def previous(self, payload: List, window: Window) -> Window:
        raise Exception("Tried to insert historical candle in previous timeframe.")


    def current(self, payload: List, window: Window) -> Window:
        raise Exception("Tried to insert historical candle in current timeframe.")


    def nexxt(self, payload: List, window: Window) -> Window:
        o = datetime(payload[0])
        c = datetime(payload[6])
        timeframe = TimeFrame(open_time=o, close_time=c)
        window.timeframes.append(timeframe)
        candle = Candle.parse_historical_candle(payload)
        window.timeframes[-1].candle = candle
        return window


class StreamCandlePipe(Pipeline):

    # required by super
    def get_close_time(self, payload: dict, window: Window) -> datetime:
        return super().round_time(datetime(payload["E"]))


    def set_last_update(self, payload: dict, window: Window) -> Window:
        candle_1m = Candle.parse_candle(payload)
        closed = bool(payload["x"])
        window._last_candle_update = candle_1m
        window._last_candle_update_closed = closed
        return window


    # required by super
    def first(self, payload: dict, window: Window) -> Window:

        if not window._last_candle_update:
            window = self.set_last_update(payload, window)
            return window

        if window.interval == Interval.SECOND_2:
            c = super().round_time(datetime(payload["E"]))
            o = c - timedelta(milliseconds=1999)
            timeframe = TimeFrame(open_time=o, close_time=c)
            window.timeframes[0] = timeframe
            candle_1m = Candle.parse_candle(payload)
            candle_2s = Candle.create_2s_candle(
                candle_1m, 
                window._last_candle_update, 
                window._last_candle_update_closed
            )
            window.timeframes[0].candle = candle_2s
            window = self.set_last_update(payload, window)
            return window

        else:
            raise Exception("Tried to insert candle from stream before history downloaded.")
        

    def update(self, payload, window, idx) -> Window:
        window.timeframes[idx].candle = Candle.update(
            candle=window.timeframes[idx].candle, 
            update=Candle.parse_candle(payload), 
            previous_update=window._last_candle_update,
            previous_update_closed=window._last_candle_update_closed
        )
        window = self.set_last_update(payload, window)
        return window


    # required by super
    def previous(self, payload: dict, window: Window) -> Window:
        if window.interval == Interval.SECOND_2:
            raise Exception("Tried to update previous 2 second timeframe.")
        window = self.update(payload, window, -2)
        return window


    # required by super
    def current(self, payload: dict, window: Window) -> Window:
        if window.interval == Interval.SECOND_2:
            raise Exception("Tried to update 2 second timeframe.")
        window = self.update(payload, window, -1)
        return window


    def add_new_timeframe(self, window) -> Window:
        timeframe = TimeFrame.create_next_timeframe(
            window.timeframes[-1].open_time, 
            window.timeframes[-1].close_time
        )
        window.timeframes.append(timeframe)
        return window


    # required by super
    def nexxt(self, payload: dict, window: Window) -> Window:
        candle = Candle.parse_candle(payload)
        if window.interval == Interval.SECOND_2:
            candle = Candle.create_2s_candle(
                candle, 
                window._last_candle_update, 
                window._last_candle_update_closed
            )
        window = self.add_new_timeframe(window)
        window.timeframes[-1].candle = candle
        window = self.set_last_update(payload, window)
        return window