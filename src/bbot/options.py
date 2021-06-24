from enum import Enum, auto
from typing import Union, Dict, List, FrozenSet
from typeguard import typechecked

class Interval(Enum):
    """name = interval, value = time in milliseconds."""

    s2:  2000
    m1:  60000
    m3:  180000
    m5:  300000
    m15: 900000
    m30: 1800000
    h1:  3600000
    h2:  7200000
    h4:  14400000
    h6:  21600000
    h8:  28800000
    h12: 43200000
    d1:  86400000
    d3:  259200000
    w1:  604800000

class Mode(Enum):
    """name = mode in uppercase, value = index+1."""

    DEBUG:   auto()
    HISTORY: auto()
    STREAM:  auto()
    PAPER:   auto()
    TESTNET: auto()
    TRADE:   auto()
    
@typechecked
class Options:
    """Bot object requires an Options object at initialization.
    This object is the public interface of Bbot.
    """
    
    def __init__(self, 
                 api_key:      str                   = ' ',
                 api_secret:   str                   = ' ',
                 mode:         str                   = 'DEBUG',
                 base_assets:  Union[str, List[str]] = 'BTC',
                 quote_assets: Union[str, List[str]] = 'USDT',
                 windows:      Dict[str, int]        = {
                     'm1'   : 500, 
                     'm15'  : 200
                    }
                 ):

        self._api_key      = api_key
        self._api_secret   = api_secret
        self._mode         = self._verify_clean_mode(mode)
        self._base_assets  = self._verify_clean_base_assets(base_assets)
        self._quote_assets = self._verify_clean_quote_assets(quote_assets)
        self._windows      = self._verify_clean_windows(windows)


    def _verify_clean_mode(mode: str) -> Mode:
        """Verifies raw user input for option `mode`"""

        if mode.upper() in Mode.__members__:
            return Mode[mode.upper()]
        else:
            raise Exception('Invalid input for option `mode` in bbot.Options')


    def _verify_clean_base_assets(base_assets: Union[str, List[str]]) -> FrozenSet[str]:
        """Verifies raw user input for option `base_assets`"""

        e = 'Invalid input for option `base_assets` or `quote_assets` in bbot.Options'

        if type(base_assets) is str:
            if (base_assets.isalpha and len(base_assets) < 10) or base_assets == '*':
                return frozenset((base_assets.upper(), ))
            else:
                raise Exception(e)
        else:
            l = len(base_assets)
            if sum([b.isalpha for b in base_assets]) == l and sum([len(b) < 10 for b in base_assets]) == l:
                return frozenset((* base_assets.upper(), ))
            else:
                raise Exception(e)


    def _verify_clean_quote_assets(self, quote_assets: Union[str, List[str]]) -> FrozenSet[str]:
        """Verifies raw user input for option `quote_assets`"""

        return self._verify_clean_base_assets(quote_assets)


    def _verify_clean_windows(windows: Dict[str, int]) -> Dict[Interval, int]:
        """Verifies raw user input for option `windows`"""

        if sum([iv in Interval.__members__ for iv in windows.keys()]) == len(windows):
            if sum([w <= 500 for w in windows.values()]) == len(windows):
                return windows

        raise Exception('Invalid input for option `windows` in bbot.Options')
        
        

    # Getters and setters

    @property
    def mode(self) -> Mode:
        return self._mode

    @property
    def base_assets(self) -> FrozenSet[str]:
        return self._base_assets

    @property
    def quote_assets(self) -> FrozenSet[str]:
        return self._quote_assets

    @property
    def windows(self) -> Dict[Interval, int]:
        return self._windows

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