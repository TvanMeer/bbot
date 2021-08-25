from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

from models.database import DataBase, Window


class Pipeline(ABC):
    """Abstract baseclass for all pipes in pipeline module."""

    def process(self, raw: Any, db: DataBase):
        """Interface for all pipelines."""

        window  = self.get_window(raw, db)
        parsed  = self.parse(raw)
        window_updated = self.insert_in_window(parsed, window)
        db_updated = self.insert_in_db(window_updated, db)
        return db_updated


    @abstractmethod
    def get_window(self, raw: Any, db: DataBase) -> Window:
        """Gets the window from the database, where `raw` should be inserted.
        The window choice is based on the symbol field and time data fields in `raw`.
        """

        raise NotImplementedError


    @abstractmethod
    def parse(self, raw: Any) -> BaseModel:
        """Turns raw data into a Pydantic Basemodel."""

        raise NotImplementedError


    @abstractmethod
    def insert_in_window(self, item: BaseModel, window: Window) -> Window:
        """Inserts this model in the corresponding window.
        Then inserts this window in the database and returns the updated database.
        """

        raise NotImplementedError


    @abstractmethod
    def insert_in_db(self, window: Window, db: DataBase) -> DataBase:
        """Inserts updated window in database."""

        raise NotImplementedError