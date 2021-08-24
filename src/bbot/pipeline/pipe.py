from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

from models.database import DataBase, Window


class Pipeline(ABC):
    """Abstract baseclass for all pipes in pipeline module."""

    def process(self, raw: Any, db: DataBase):
        """Interface for all pipelines."""

        window = self.get_window(raw, db)
        parsed = self.parse(raw)
        db     = self.insert(parsed, window)
        return db


    @abstractmethod
    def get_window(self, raw: Any, db: DataBase) -> Window:
        """Gets the window where `raw` should be inserted
        from database, based on symbol field and time data in raw data.
        """

        raise NotImplementedError


    @abstractmethod
    def parse(self, raw: Any) -> BaseModel:
        """Turns raw data into a Pydantic Basemodel."""

        raise NotImplementedError


    @abstractmethod
    def insert(self, item: BaseModel, window: Window) -> DataBase:
        """Inserts this model in window.
        Then inserts the window in database and returns database.
        """

        raise NotImplementedError