'''

Binance client implementation

'''
from typing import Any, Dict, List, Set

from binance import AsyncClient

from . import base_client
from .. import options


class BinanceClient(base_client.BaseClient):
    
    def __init__(self, options: options.Options):
        super().__init__(options)

    async def _create_async_client(options: options.Options) -> Any:
        client = await AsyncClient.create(api_key    = options.api_key, 
                                          api_secret = options.api_secret)
        return client

    async def _download_all_symbols(self, client: AsyncClient) -> List[Dict]:
        raw = await client.get_all_tickers()
        return raw


    def _parse_all_symbols(raw: List[Dict]) -> Set[str]:
        pass

    async def _download_history(client: AsyncClient) -> Any:
        pass

    def _parse_history(raw: Any) -> List[Dict[str, float]]:
        pass

    async def _start_candle_sockets(client: AsyncClient) -> None:
        pass

    def _parse_candle(raw: Dict) -> Dict:
        pass

    async def _start_user_socket(client: AsyncClient) -> None:
        pass

    def _parse_user_event(event: Any) -> Dict:
        pass