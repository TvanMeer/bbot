# bbot

A simple framework to build Binance spot trading bots

---PRE-ALPHA---

## Description

---

Bbot is a microframework for building homebrew Binance trade bots. It provides a higher level of abstraction on top of [python-binance](https://python-binance.readthedocs.io/en/latest/index.html). Bbot streams [candlestick data](https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-streams) from Binance and provides basic functionality to work with this data and act upon changes in realtime.

## Features

---

- Download historical candlestick data and update it realtime through a websocket.
- Do this for many timeframes simultaniously, like 2s, 1m and 15m timeframes.
- Work with many assets simultaniously.
- Automatic parsing, cleaning and type conversion.
- Automatic conversion to dictionaries, Pandas timeseries or Numpy array.
- Automatic data integrity checking and safety guards on trading behavior.
- Feature engineering pipeline.
- Build, analize and manage trade strategies in real time.

## Installation

---

TODO

## Usage

---

### Step 1 - Set options

Start by specifying the options of Bbot by creating an instance of the `bbot.Options()` class.

```
from bbot import Options

options = Options(mode = 'PAPER',
                  base_assets  = ['BTC',],
                  quote_assets = ['USDT',],
                  windows = {'1m' : 500,
                             '15m': 200
                             }
                  )

```

You can also set the options like this:

```
from bbot import Options

options = Options()

options.mode = 'STREAM'
options.base_assets  = ['BTC',]
options.quote_assets = ['USDT',]
options.windows = {'1m' : 500,
                   '15m': 200
                   }

```

Possible options:

| Parameter    | Options                                     | Description                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------ | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mode         | `'HISTORY'`                                 | Download only historical candle data. Do not start realtime datastream.                                                                                                                                                                                                                                                                                                                                        |
|              | `'STREAM'`                                  | Download historical candle data and update this data realtime through a websocket.                                                                                                                                                                                                                                                                                                                             |
|              | `'PAPER'`                                   | Like STREAM, but also simulate trading mode without actually starting a trade client.                                                                                                                                                                                                                                                                                                                          |
|              | `'TESTNET'`                                 | Like PAPER, but papertrade on the Binance Testnet. Useful if you want to test the trade client.                                                                                                                                                                                                                                                                                                                |
|              | `'TRADE'`                                   | Put your bot into production and trade with real money.                                                                                                                                                                                                                                                                                                                                                        |
| base_assets  | e.g. `'BTC'` or `['BTC', 'ETH']` or `'*'`   | A single string or list of strings, representing the left asset in all pairs trading on Binance. `'*'` represents all base assets trading on Binance.                                                                                                                                                                                                                                                          |
| quote_assets | e.g. `'USDT'` or `['USDT', 'BTC']` or `'*'` | A single string or list of strings, representing the right asset in all pairs trading on Binance. `'*'` represents all quote assets trading on Binance.                                                                                                                                                                                                                                                        |
| windows      | e.g. `{'1m': 500, '15m': 200}`              | A dictionary with key=timeframe and value=number of candles. In this example Bbot will download the last 500 minutes of 1 minute candles and the last 50 hours of 15 minute candles. The following timeframes are supported: 2s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M. Note that Bbot can not download 2s history, but only accumulates 2s candles until the window reaches max size. |

### Step 2 - Start Bbot

Create an instance of the `bbot.Bot()` class with the options specified in step 1.  
Add your credentials to use the Binance API.

```
from bbot import Bot


key    = 'djeZKZM5fThTGFIWNVJvyHzkQJfzbMCpACNgI8AVYmcT52hBgct3mikj3tZ7AXig'
secret = 'TEPbhxIlqXsjaIJ45TwN86b01lt3XOe40WcAWdT4v0gghDrf7Tw8nV6WG4ohSb0v'

bot    = Bot(api_key=key, api_secret=secret, options=options)

```

### Step 3 - Data exploration

Let's explore the data Bbot provides to work with.  
Because in step 1 we specified BTC as the base asset and USDT as the quote asset, Bbot only downloaded data for the pair 'BTCUSDT'.  
Our bot instance has the attribute 'pairs', which is a dictionary with key=symbol and value= a `bbot.Pair()` object.

```
len(bot.pairs)
bot.pairs

```

```
>>> 1
>>> {'BTCUSDT': <__main__.Pair object at 0x7f473eed8ee0>}

```

The `'bbot.Pair()'` object contains all realtime data related to the trading pair 'BTCUSDT'.  
The attributes `bbot.Pair.candles_1m` and `bbot.Pair.candles_15m` contain our candlestick data.  
Candlestick data is hold in a list of dicts, each dict representing one candle.

```
btc = bot.pairs['BTCUSDT']

btc.symbol
btc.price
len(btc.candles_1m)     # A 500 candle window was specified in options
type(btc.candles_1m)    # The last 500 candles in chronological order

```

```
>>> BTCUSDT
>>> 37945.24978
>>> 500
>>> <class 'list'>

```

Lets print the last 15 minute candle, that updates every 2 seconds. The other candles in our 200 candle, 15 minute frame are already closed, so they are not updated anymore.  
The last candle in every window is being updated every 2 seconds.

```
import json
import time

last_candle = btc.candles_15m[-1]
json.dumps(last_candle, indent=4)

time.sleep(2)

last_candle = btc.candles_15m[-1]
json.dumps(last_candle, indent=4)

```

```
>>> TODO
```

You can convert a candlestick window to a Pandas dataframe or Numpy array like this:

```
df     = btc.to_df('1m')
np_arr = btc.to_np('1m')

```

### Step 4 (optional) - Feature engineering

TODO

### Step 5 - Define a trading strategy

Based on the data that is being streamed, your bot makes the decision to either buy, sell or do nothing.

Here is an example of an implementation of a very simple strategy:

If the current price is > 1% of the close price in the previous 15 minute candle, then buy bitcoin, with 10% of the total investment capital of the corresponding quote asset in your account.
If the price has dropped with 1% since the close time of the previous 15 minute candle, then sell all bitcoin in your portfolio.

In this case, if you have 100 USDT in your account, then buy for 10 USDT bitcoin if the price increases with 1% and sell all bitcoin if it drops with 1%.

```
def your_strategy(bot):

    # Example strategy
    window = bot.pairs['BTCUSDT'].candles_15m
    current_candle  = window[-1]
    previous_candle = window[-2]

    if current_candle['close'] > previous_candle['close'] * 1.01:
       bot.buy('BTCUSDT', cap_percentage=10)
    if current_candle['close'] < previous_candle['close'] / 1.01:
       bot.sell('BTCUSDT', cap_percentage=100)

```

### Step 6 - Run trading strategy

Now a strategy is defined, let's run it, at a specified interval in seconds.
In this example `your_strategy` runs every minute, starting at the first candle after the opening of each 15 minute candle.  
`every_n_seconds` needs to be an even number.

```
bot.run_strategy(your_strategy, interval='15m', every_n_seconds=60)

```

You can add multiple strategies, running simultaniously.  
If you don't want a strategy to run at a specified interval, but customize when it should run, you can pass a function to the interval parameter instead.
This function is executed every 2 seconds, at each candle update.  
It needs to return a bool: execute `your_strategy` or not.  
In this example `your_strategy` runs every 6th second after a new 1 minute candle is opened.  
It uses the `n_updates` field, a field that is injected by Bbot in each candle.

```
def custom_timer(bot):
    if bot.pairs['BTCUSDT'].candles_1m[-1]['n_updates'] == 3:
        return True
    else:
        return False


bot.run_strategy(your_strategy, interval=custom_timer)

```

Immediately after you add your strategy, Bbot will start trading with that strategy in case you specified option 'mode' to be 'TRADE'.

### Step 7 - Analyze trading strategy performance

The performance of all trading strategies can be monitored realtime.  
This is done by implementing a listener function. A potential usecase might be to send this data to a gui or webservice. Bbot accepts only one metrics listener function.

```
def your_analyzer(metrics_stream):
    print(metrics_stream)


bot.start_metrics_listener(your_analyzer)

```

```
>>> TODO
>>>
>>>

```

### Complete example

```
from bbot import Options, Bot

# Define options
options = Options(mode = 'PAPER',
                  base_assets  = ['BTC',],
                  quote_assets = ['USDT',],
                  windows = {'1m' : 500,
                             '15m': 200
                             }
                  )

# Start to download and stream data
key    = 'djeZKZM5fThTGFIWNVJvyHzkQJfzbMCpACNgI8AVYmcT52hBgct3mikj3tZ7AXig'
secret = 'TEPbhxIlqXsjaIJ45TwN86b01lt3XOe40WcAWdT4v0gghDrf7Tw8nV6WG4ohSb0v'
bot = Bot(api_key=key, api_secret=secret, options=options)


# Some random example trading strategy
def your_strategy(bot):

    window = bot.pairs['BTCUSDT'].candles_15m
    current_candle  = window[-1]
    previous_candle = window[-2]

    if current_candle['close'] > previous_candle['close'] * 1.01:
       bot.buy('BTCUSDT', cap_percentage=10)
    if current_candle['close'] < previous_candle['close'] / 1.01:
       bot.sell('BTCUSDT', cap_percentage=100)


# Run the above strategy every 60 seconds
bot.add_strategy(your_strategy, interval=60)

# Specify a function to inspect the performance of your bot
def your_analyzer(metrics_stream):
    print(metrics_stream)

# Start inspecting
bot.start_metrics_listener(your_analyzer)

```

## API reference

TODO
