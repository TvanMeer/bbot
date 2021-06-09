"""

All data and logic related to a pair

"""

class Pair():

    def __init__(self, symbol, options):
        self.symbol  = symbol
        self.options = options

        self._historical_windows_downloaded = 0
    
    def _add_historical_window(self, interval, raw):
        if len(raw) != self.options.windows[interval]:
            print(f'Error: BinanceAPI returned {len(raw)} candles instead of {self.windowsize} for interval {interval}')

        parsed = []
        for c in raw:
            candle = {
                'open_time':   float(c[0]),
                'open':        float(c[1]),
                'high':        float(c[2]),
                'low':         float(c[3]),
                'close':       float(c[4]),
                'volume':      float(c[5]),
                'close_time':  float(c[6]),
                'qa_volume':   float(c[7]),
                'n_trades':    float(c[8]),
                'tbba_volume': float(c[9]),
                'tbqa_volume': float(c[10])
            }
            parsed.append(candle)
        
        setattr(self, 'candles_' + interval, parsed)
        self._historical_windows_downloaded += 1

        print(parsed)
        print('++++++++++++++++++++++++++++++++++++++++++')


    def _add_candle(self, raw):

        if self._historical_windows_downloaded != len(self.options.windows.keys()):
            pass
        symbol = raw['data']['s']
        d = raw['data']['k']
        candle = {
            'open_time':   float(d['t']),
            'open':        float(d['o']),
            'high':        float(d['h']),
            'low':         float(d['l']),
            'close':       float(d['c']),
            'volume':      float(d['v']),
            'close_time':  float(d['T']),
            'qa_volume':   float(d['q']),
            'n_trades':    float(d['n']),
            'tbba_volume': float(d['V']),
            'tbqa_volume': float(d['Q'])
        }

        print(candle, '--------------------------------')
        