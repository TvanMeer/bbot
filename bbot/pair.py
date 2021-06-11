"""

All data and logic related to a pair

"""

class Pair():

    def __init__(self, symbol, options):
        self.symbol  = symbol
        self.options = options
        self._ot_delta = {
            '2s':  2000,
            '30s': 30000,
            '1m':  60000,
            '3m':  180000,
            '5m':  300000,
            '15m': 900000,
            '30m': 1800000,
            '1h':  3600000,
            '2h':  7200000,
            '4h':  14400000,
            '6h':  21600000,
            '8h':  28800000,
            '12h': 43200000,
            '1d':  86400000,
            '3d':  259200000,
            '1w':  604800000,
            '1M':  2678400000
        }

    
    def _add_historical_window(self, interval, raw):
        if len(raw) != self.options.windows[interval]:
            print(f'Error: BinanceAPI returned {len(raw)} candles instead of {self.options.windows[interval]} for interval {interval}')

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
                'tbqa_volume': float(c[10]),
                'corrupt':     False
            }
            if len(parsed) > 0:
                candle = self._verify_new_candle(parsed, interval, candle)
            parsed.append(candle)
        
        setattr(self, 'candles_' + interval, parsed)

        print('Historical window parsed...')

    def _verify_new_candle(self, window, interval, candle):
        
        prev_candle = window[-1]
        e = f'Data corruption in {self.symbol} {interval} candles in field '
        
        ot  = candle['open_time']
        pot = prev_candle['open_time']
        ct  = candle['close_time']
        pct = prev_candle['close_time']
        if ot <= pot or ot <= pct:
            candle['corrupt'] = True
            raise Exception(e + 'open_time')
        # ... TODO
        return candle


    def _parse_candle(self, raw):

        for iv in self.options.windows.keys():
            if hasattr(self, 'candles_' + iv):

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
                    'tbqa_volume': float(d['Q']),
                    'corrupt':     False
                }

                window = getattr(self, 'candles_' + iv)
                prev_candle = window[-1]
                if candle['open_time'] - prev_candle['open_time'] == self._ot_delta[iv]:
                    self._insert_candle(candle, window, iv)
                else:
                    self._update_candle(candle, window, iv)


    def _insert_candle(self, candle, window, interval):

        candle = self._verify_new_candle(window, interval, candle)
        candle['close_time'] = candle['open_time'] + (self._ot_delta[interval] -1)
        # Roll window
        window.append(candle)
        del window[0]
        setattr(self, 'candles_' + interval, window)

        print('candle inserted')


    def _update_candle(self, candle, window, interval):
        
        prev_candle = window[-1]

        # Validate updates for previous candle
        e  = f'Missing data/ data corruption in {self.symbol} {interval} candles in field '

        ot  = candle['open_time']
        pot = prev_candle['open_time']
        ct  = candle['close_time']
        pct = prev_candle['close_time']

        if ot < pot or ot > pct:
            prev_candle['corrupt'] = True
            raise Exception(e + 'open_time')
        if ct > pct or ct < pot:
            prev_candle['corrupt'] = True
            raise Exception(e + 'close_time')
        # ... TODO

        # Update fields in previous candle
        prev_candle['high'] = candle['high'] if candle['high'] > prev_candle['high'] else prev_candle['high']
        prev_candle['low']  = candle['low']  if candle['low']  > prev_candle['low']  else prev_candle['low']
        prev_candle['close']= candle['close']
        # ... TODO

        # Replace previous candle
        window[-1] = prev_candle
        setattr(self, 'candles_' + interval, window)

        print('candle updated')
        