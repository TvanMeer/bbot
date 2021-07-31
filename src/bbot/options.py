from typing import Union, Dict, List


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

        self._POSSIBLE_INTERVALS = {
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

        self._POSSIBLE_MODES = {
            "DEBUG",
            "HISTORY",
            "STREAM",
            "PAPER",
            "TESTNET",
            "TRADE",
        }

        self._api_key = api_key
        self._api_secret = api_secret
        self._mode = mode
        self._base_assets = base_assets
        self._quote_assets = quote_assets
        self._windows = windows

    # Getters
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
    def base_assets(self) -> set[str]:
        return self._base_assets

    @property
    def quote_assets(self) -> set[str]:
        return self._quote_assets

    @property
    def windows(self) -> Dict[str, int]:
        return self._windows

    # Setters
    def _error(self, attr_name):
        raise Exception(
            f"Invalid input for option `{attr_name}` in bbot.Options"
        )

    def _validate_credential(self, attr_name, cred):
        if cred == " ":
            pass
        elif len(cred) != 64:
            self._error(attr_name)
        else:
            for char in cred:
                if not (char.isalpha() or char.isdigit()):
                    self._error(attr_name)

    @api_key.setter
    def api_key(self, key):
        self._validate_credential("api_key", key)
        self._api_key = key

    @api_secret.setter
    def api_secret(self, secret):
        self._validate_credential("api_secret", secret)
        self._api_secret = secret

    @mode.setter
    def mode(self, mode: str):
        m = mode.upper()
        if m in self._POSSIBLE_MODES:
            self._mode = m
        else:
            self._error("mode")

    def _set_assets(self, attr, a):
        def validate(attr, asset):
            checks = [
                type(asset) is str,
                asset.isalpha(),
                len(asset) < 10,
            ]
            if sum(checks) == 3:
                return asset.upper()
            else:
                self._error(attr)

        def set_asset(attr, asset):
            setattr(self, "_" + attr, asset)

        if a == "*":
            set_asset(attr, ["*"])
        elif type(a) is str:
            v = validate(attr, a)
            set_asset(attr, [v])
        elif type(a) is list:
            checked = []
            [checked.append(validate(attr, asset)) for asset in a]
            set_asset(attr, checked)
        else:
            self._error(attr)

    @base_assets.setter
    def base_assets(self, base_assets: Union[str, List[str]]):
        self._set_assets("base_assets", base_assets)

    @quote_assets.setter
    def quote_assets(self, quote_assets: Union[str, List[str]]):
        if quote_assets == "*" and self.base_assets == ["*"]:
            raise Exception("Cannot use * for both base and quote assets")
        self._set_assets("quote_assets", quote_assets)

    @windows.setter
    def windows(self, windows: Dict[str, int]):
        intervals = set(windows.keys())
        winsizes = set(windows.values())

        def validate_interval(interval):
            possible = set(self._POSSIBLE_INTERVALS.keys())
            if not interval in possible:
                self._error("window")

        def validate_winsize(winsize):
            checks = [
                type(winsize) is int,
                winsize <= 500,
                winsize % 2 == 0,
            ]
            if sum(checks) != 3:
                self._error("window")

        [validate_interval(iv) for iv in intervals]
        [validate_winsize(w) for w in winsizes]
        self._windows = windows
