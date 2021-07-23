from typing import Union, Dict, List, FrozenSet


class Options:
    """Bot object requires an Options object at initialization.
    This object is the public interface of Bbot.
    """

    def __init__(
        self,
        api_key: str = " ",
        api_secret: str = " ",
        mode: str = "DEBUG",
        base_assets: Union[str, List[str]] = "BTC",
        quote_assets: Union[str, List[str]] = "USDT",
        windows: Dict[str, int] = {"1m": 500, "15m": 200},
    ):

        self._possible_intervals = {
            "2s": 2000,
            "1m": 60000,
            "3m": 180000,
            "5m": 300000,
            "15m": 900000,
            "30m": 1800000,
            "1h": 3600000,
            "2h": 7200000,
            "4h": 14400000,
            "6h": 21600000,
            "8h": 28800000,
            "12h": 43200000,
            "1d": 86400000,
            "3d": 259200000,
            "1w": 604800000,
        }
        self._possible_modes = frozenset(
            ["DEBUG", "HISTORY", "STREAM", "PAPER", "TESTNET", "TRADE"]
        )

        self._api_key = api_key
        self._api_secret = api_secret
        self._mode = self._verify_clean_mode(mode)
        self._base_assets = self._verify_clean_base_assets(base_assets)
        self._quote_assets = self._verify_clean_quote_assets(quote_assets)
        self._windows = self._verify_clean_windows(windows)

    def _verify_clean_mode(self, mode: str) -> str:
        """Verifies raw user input for option `mode`"""

        if mode.upper() in self._possible_modes:
            return mode.upper()
        else:
            raise Exception(
                f"Invalid input for option `mode` in bbot.Options: {mode}"
            )

    def _verify_clean_base_assets(
        self, base_assets: Union[str, List[str]]
    ) -> FrozenSet[str]:
        """Verifies raw user input for option `base_assets`"""

        e = "Invalid input for option `base_assets` or `quote_assets` in bbot.Options"

        if type(base_assets) is str:
            if (
                base_assets.isalpha() and len(base_assets) < 10
            ) or base_assets == "*":
                return frozenset((base_assets.upper(),))
            else:
                raise Exception(e)
        else:
            l = len(base_assets)

            if (
                sum([b.isalpha() for b in base_assets]) == l
                and sum([len(b) < 10 for b in base_assets]) == l
            ):
                return frozenset([b.upper() for b in base_assets])
            else:
                raise Exception(e)

    def _verify_clean_quote_assets(
        self, quote_assets: Union[str, List[str]]
    ) -> FrozenSet[str]:
        """Verifies raw user input for option `quote_assets`"""

        return self._verify_clean_base_assets(quote_assets)

    def _verify_clean_windows(self, windows: Dict[str, int]) -> Dict[str, int]:
        """Verifies raw user input for option `windows`"""

        if sum(
            [iv in self._possible_intervals for iv in windows.keys()]
        ) == len(windows):
            if sum([w <= 500 for w in windows.values()]) == len(windows):
                if sum([w % 2 == 0 for w in windows.values()]) == len(windows):
                    return windows

        raise Exception("Invalid input for option `windows` in bbot.Options")

    # Getters and setters
    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def api_secret(self) -> str:
        return self._api_secret

    @property
    def mode(self) -> str:
        return self._mode

    @property
    def base_assets(self) -> FrozenSet[str]:
        return self._base_assets

    @property
    def quote_assets(self) -> FrozenSet[str]:
        return self._quote_assets

    @property
    def windows(self) -> Dict[str, int]:
        return self._windows

    @property
    def possible_intervals(self) -> Dict[str, int]:
        return self._possible_intervals

    @property
    def possible_modes(self) -> FrozenSet[str]:
        return self._possible_modes

    @mode.setter
    def mode(self, mode: str) -> None:
        self._mode = self._verify_clean_mode(mode)

    @base_assets.setter
    def base_assets(self, base_assets: Union[str, List[str]]) -> None:
        self._base_assets = self._verify_clean_base_assets(base_assets)

    @quote_assets.setter
    def quote_assets(self, quote_assets: Union[str, List[str]]) -> None:
        self._quote_assets = self._verify_clean_quote_assets(quote_assets)

    @windows.setter
    def windows(self, windows: Dict[str, int]) -> None:
        self._windows = self._verify_clean_windows(windows)
