"""

Public API to set options of bbot.

"""
class Options():
    
    def __init__(self, 
                 mode        = 'PAPER',
                 base_assets =['BTC', ],
                 quote_assets=['USDT', ],
                 windows     ={'1m' : 500, 
                               '15m': 200}
                 ):

        self.mode         = self._verify_mode(mode)
        self.base_assets  = self._verify_base_assets(base_assets)
        self.quote_assets = self._verify_quote_assets(quote_assets)
        self.windows      = self._verify_windows(windows)


    def _verify_mode(self, mode):
        m = mode.upper()
        if m in {'DEBUG', 
                 'HISTORY', 
                 'STREAM', 
                 'PAPER', 
                 'TESTNET', 
                 'TRADE'}:
            return m
        else:
            e = f'''Invalid input for bbot option `mode`.
            Choose either DEBUG, HISTORY, STREAM, PAPER, TESTNET or TRADE.'''
            raise Exception(e)


    def _verify_base_assets(self, ba):

        # Only verifies types    
        e = f'''Invalid input for bbot option 'base_assets'.
        Should be a list of strings, such as ['BTC', 'ETH']'''
        if ba == '*':
            return '*'
        elif type(ba) is str:
            return [ba.upper(), ]
        elif type(ba) is list:
            if all(isinstance(item, str) for item in ba):
                [a.upper() for a in ba]
                return ba
            else:
                raise Exception(e)
        else:
            raise Exception(e)


    def _verify_quote_assets(self, qa):

        # Only verifies types
        e = f'''Invalid input for bbot option 'quote_assets'.
            Should be a list of strings, such as ['USDT',]'''
        if qa == '*':
            return '*'
        elif type(qa) is str:
            return [qa.upper(), ]
        elif type(qa) is list:
            if all(isinstance(item, str) for item in qa):
                [a.upper() for a in qa]
                return qa
            else:
                raise Exception(e)
        else:
            raise Exception(e)

    
    def _verify_windows(self, windows):

        possible_windows = ['2s', '1m', '3m', '5m', '15m', '30m',
                            '1h', '2h', '4h', '6h', '8h', '12h', 
                            '1d', '3d', '1w', '1M']

        e = '''Invalid input for bbot option 'windows'.
            Should be a dict, with k=interval and v=windowsize.
            E.g. {'1m': 500, '30m': 100}'''

        for k, v in windows.items():
            if not type(k) is str or not type(v) is int:
                raise Exception(e)
            if k not in possible_windows:
                raise Exception(e)
        return windows