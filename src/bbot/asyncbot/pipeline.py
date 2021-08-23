from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel

from models.database import DataBase


class PipeLine(ABC):

    @abstractmethod
    def parse(self, raw: Any) -> BaseModel:
        """Turns raw data into a Pydantic Basemodel."""
        return NotImplementedError


    @abstractmethod
    def insert(self, item: BaseModel, db: DataBase):
        """Inserts this model in the database instance."""
        return NotImplementedError


    def process(self, raw: Any, db: DataBase):
        """Interface for all pipelines."""
        parsed = self.parse(raw)
        self.insert(parsed, db)