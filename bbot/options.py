"""

Public API to set options of bbot.

"""


class Options():

    def __init__(self, mode='STREAM',
                 base_assets=['BTC', ],
                 quote_assets=['USDT', ],
                 windows={'1m': 200, '1d': 10}
                 ):

        self.mode = self._verify_mode(mode)
        self.base_assets = self._verify_base_assets(base_assets)
        self.quote_assets = self._verify_quote_assets(quote_assets)
        self.windows = self._verify_windows(windows)

    @property
    def mode(self):
        return self.mode

    @mode.setter
    def mode(self, mode):
        self.mode = self._verify_mode(mode)

    @property
    def base_assets(self):
        return self.base_assets

    @base_assets.setter
    def base_assets(self, ba):
        self.base_assets = self._verify_base_assets(ba)

    @property
    def quote_assets(self):
        return self.quote_assets

    @quote_assets.setter
    def quote_assets(self, qa):
        self.quote_assets = self._verify_quote_assets(qa)

    @property
    def windows(self):
        return self.windows

    @windows.setter
    def windows(self, windows):
        self.windows = self._verify_windows(windows)

    def _verify_mode(self, mode):
        m = mode.upper()
        if m in {'HISTORY', 'STREAM', 'PAPER', 'TESTNET', 'TRADE'}:
            return m
        else:
            e = f'''Invalid input for bbot option `mode`.
            Choose either HISTORY, STREAM, PAPER, TESTNET or TRADE.
            Your given input is: {mode}'''
            raise Exception(e)

    def _verify_base_assets(self, ba):

        e = f'''Invalid input for bbot option 'base_assets'.
            Should be a list of strings, such as ['BTC', 'ETH']
            Your given input is {ba}'''
        if ba == '*':
            return [ba, ]
        elif type(ba) is str:
            return [ba.upper(), ]
        elif type(ba) is list:
            if all(isinstance(item, str) for item in ba):
                [b.upper() for b in ba]
                return ba
            else:
                raise Exception(e)
        else:
            raise Exception(e)

    def _verify_quote_assets(self, qa):

        e = f'''Invalid input for bbot option 'quote_assets'.
            Should be a list of strings, such as ['USDT',]
            Your given input is {qa}'''
        if qa == '*':
            return [qa, ]
        elif type(qa) is str:
            return [qa.upper(), ]
        elif type(qa) is list:
            if all(isinstance(item, str) for item in qa):
                [b.upper() for b in qa]
                return qa
            else:
                raise Exception(e)
        else:
            raise Exception(e)

    def _verify_windows(self, windows):

        possible_windows = ['2s', '30s', '1m', '3m', '5m', '15m', '30m',
                            '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1m']

        e = '''Invalid input for bbot option 'windows'.
            Should be a dict, with k=interval and v=windowsize.
            E.g. {'1m': 500, '30m': 100}'''

        for k, v in windows.items():
            if not type(k) is str or not type(v) is int:
                raise Exception(e)
            if k not in possible_windows:
                raise Exception(e)
        return windows
