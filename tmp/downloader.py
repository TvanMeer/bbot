"""Temporary script to download relevant data for usage in test fixtures.
"""
import asyncio

from binance import AsyncClient, BinanceSocketManager

async def main():

    # initialise the client
    client = await AsyncClient.create()

    # initialise websocket factory manager
    bm = BinanceSocketManager(client)

    us = bm.user_socket()
    async with us as stream:
        while True:
            msg = await stream.recv()
            print(msg)


    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())