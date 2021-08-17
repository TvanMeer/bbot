from abc import ABC, abstractmethod
from typing import Any, Dict, List
from binance import Client
from pydantic import BaseModel

from ..models.database import DataBase
from ..models.options import Options


class DataProcessor(ABC):
    """Processes a single field of data, such as database.all_symbols, database.transactions etc."""

    @abstractmethod
    def download(self, client: Client) -> Any:
        pass

    @abstractmethod
    def parse(self, raw_data: Any) -> BaseModel:
        pass

    @abstractmethod
    def insert(self, obj: BaseModel, db: DataBase):
        pass


class SymbolProcessor(DataProcessor):
    def download(self, client: Client) -> List[Dict[str, str]]:
        pass

    def parse(self, tickers: List[Dict[str, str]]) -> BaseModel:
        pass

    def insert(self, symbols: BaseModel, db: DataBase):
        pass


class Downloader:
    """Downloads all required data from Binance that is not realtime.
    Examples are account balance, transaction history, symbols traded on Binance etc.
    This class also interfaces all processing logic for that data.
    """

    def __init__(self, options: Options):
        if options.mode == options.Mode.test:
            pass
        else:
            self.database = DataBase(options)

            # Download market info
            client = Client(options.key, options.secret)
            self.database = self.download_market_info(client, self.database)

            # Download account info if option `paper` or `trade` is selected
            if (
                options.mode == options.Mode.paper
                or options.mode == options.Mode.trade
            ):
                self.database = self.download_account_info(
                    client, self.database
                )

    def download_market_info(
        self, client: Client, database: DataBase
    ) -> DataBase:
        # TODO
        return database

    def download_account_info(
        self, client: Client, database: DataBase
    ) -> DataBase:
        # TODO
        return database

    def get_database(self) -> DataBase:
        return self.database
