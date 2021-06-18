'''

Binance client implementation

'''
from . import base_client


class BinanceClient(base_client.BaseClient):
    
    def __init__(self):
        super().__init__()