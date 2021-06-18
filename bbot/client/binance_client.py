'''

Binance client implementation

'''

from typing import Any, Dict, List, Set
from binance import AsyncClient

from .base_client      import BaseClient
from ..options         import Options
from ..data.candle     import Candle
from ..data.user_event import UserEvent


class BinanceClient(BaseClient):
    
    def __init__(self, options: Options):
        super().__init__(options)

    async def _create_async_client(options: Options) -> AsyncClient:
        client = await AsyncClient.create(api_key    = options.api_key, 
                                          api_secret = options.api_secret)
        return client

    async def _download_all_symbols(self, client: AsyncClient) -> List[Dict]:
        raw = await client.get_all_tickers()
        return raw


    def _parse_all_symbols(raw: List[Dict]) -> Set[str]:
        pass

    async def _download_history(client: AsyncClient) -> List[List]:
        pass

    def _parse_history(raw: Any) -> List[Candle]:
        pass

    async def _start_candle_sockets(client: AsyncClient) -> None:
        pass

    def _parse_candle(raw: Dict) -> Candle:
        pass

    async def _start_user_socket(client: AsyncClient) -> None:
        pass

    def _parse_user_event(event: Any) -> UserEvent:
        pass