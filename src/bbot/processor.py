import logging
from typing import Any

from .database import Database
from .options import Options


class _BaseProcessor:
    def process(
        self, datatype: str, raw_data: Any, database: Database
    ) -> None:
        parsed_data = self.parse(raw_data)
        logging.debug(f"Parsed {datatype}.")

        validated_data = self.validate(parsed_data, database)
        logging.debug(f"Validated {datatype}.")

        filtered_data = self.filterr(validated_data, database.options)
        logging.debug(f"Filtered {datatype}.")

        updated_db = self.insert(filtered_data, database)
        logging.debug(f"Inserted {datatype}.")

        return updated_db

    def parse(self, raw_data: Any) -> dict:
        raise NotImplementedError

    def validate(self, parsed_data: dict, database) -> dict:
        raise NotImplementedError

    def filterr(self, validated_data: dict, options: Options) -> dict:
        raise NotImplementedError

    def insert(self, filtered_data: dict, database: Database) -> Database:
        raise NotImplementedError


class _SymbolProcessor(_BaseProcessor):
    pass


class _HistoricalCandleProcessor(_BaseProcessor):
    pass


class _StreamedCandleProcessor(_BaseProcessor):
    pass


class _StreamedMiniTickerProcessor(_BaseProcessor):
    pass


class _StreamedTickerProcessor(_BaseProcessor):
    pass


class _DepthProcessor(_BaseProcessor):
    pass
