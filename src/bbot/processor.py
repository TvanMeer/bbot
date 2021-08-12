import logging
from typing import Any, List

from .database import Database
from .options import Options


class _BaseProcessor:
    """Usage:

    Processors are instantiated in separate coroutines inside the class AsyncBot.
    All of them are used like this:

    cp = _CandleProcessor()
    self.database = cp.process(candle, self.database)
    """

    def pipe(
        self, datatype: str, raw_data: Any, database: Database
    ) -> Database:
        parsed_data = self.parse(raw_data)
        logging.debug(f"Parsed {datatype}.")

        validated_data = self.validate(parsed_data, database)
        logging.debug(f"Validated {datatype}.")

        filtered_data = self.filterr(validated_data, database.options)
        logging.debug(f"Filtered {datatype}.")

        updated_db = self.insert(filtered_data, database)
        logging.debug(f"Inserted {datatype}.")

        return updated_db

    def process(self, raw_data: Any, database: Database) -> Database:
        raise NotImplementedError

    def parse(self, raw_data: Any) -> Any:
        raise NotImplementedError

    def validate(self, parsed_data: Any, database: Database) -> Any:
        raise NotImplementedError

    def filterr(self, validated_data: Any, options: Options) -> Any:
        raise NotImplementedError

    def insert(self, filtered_data: Any, database: Database) -> Database:
        raise NotImplementedError


class _SymbolProcessor(_BaseProcessor):
    def process(self, tickers_list: List, database: Database) -> Database:
        return super().pipe("symbol", tickers_list, database)

    def process_all_symbols(
        self, tickers_list: List, database: Database
    ) -> Database:
        parsed = self.parse(tickers_list)
        validated = self.validate(parsed, database)
        database.ALL_SYMBOLS = validated
        return database

    def parse(self, raw_data: List) -> set:
        symbols = set()
        for ticker in raw_data:
            symbols.add(ticker["symbol"])
        return symbols

    def validate(self, parsed_data: set, database: Database) -> set:
        if len(parsed_data) > 50:
            return parsed_data
        else:
            raise Exception("Could not download all tickers from Binance.")

    def filterr(self, validated_data: set, options: Options) -> set:

        selected = set()

        def exact_match(sym, base, quote):

            if "*" in [base, quote]:
                selected.add(sym)
            else:
                left = sym[: len(base)]
                right = sym[len(base) :]
                if left == base and right == quote:
                    selected.add(sym)

        for sym in validated_data:
            for base in options.base_assets:
                if sym.startswith(base) or base == "*":
                    for quote in options.quote_assets:
                        if sym.endswith(quote) or quote == "*":
                            exact_match(sym, base, quote)

        return selected

    def insert(self, filtered_data: set, database: Database) -> Database:
        database.SELECTED_SYMBOLS = filtered_data
        return database


class _HistoricalCandleProcessor(_BaseProcessor):
    def process(self, historical_candle: List, database: Database) -> Database:
        return super().pipe("historical_candle", historical_candle, database)


class _StreamedCandleProcessor(_BaseProcessor):
    def process(self, candle: dict, database: Database) -> Database:
        return super().pipe("candle", candle, database)


class _StreamedMiniTickerProcessor(_BaseProcessor):
    def process(self, minitick: dict, database: Database) -> Database:
        return super().pipe("minitick", minitick, database)


class _StreamedTickerProcessor(_BaseProcessor):
    def process(self, tick: dict, database: Database) -> Database:
        return super().pipe("tick", tick, database)


class _DepthProcessor(_BaseProcessor):
    def __init__(self, resolution):
        self.resolution = resolution
        super().__init__()

    def process(self, depthchart: List, database: Database) -> Database:
        return super().pipe("depth" + self.resolution, depthchart, database)
