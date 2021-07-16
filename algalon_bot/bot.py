from typing import Type
from algalon_bot.modules.client import Client
import algalon_bot.settings as settings
import algalon_bot.modules.messages.messages as messages
import asyncio

async def trade_loop(client):
    await asyncio.gather(
        client.producer(messages.auth_msg()), 
        client.producer(messages.heartbeat_msg())
    )
    while True:
        print("Bot started")
        if not client.get_switch():
            initial_price = client.ticker.get_buy_price()
            await client.producer(messages.buy_msg(client, initial_price))
            while True:
                await client.producer(messages.order_status_msg(client))
                if client.get_order_state() == 'filled':
                    client.switch()
                    break
                elif client.ticker.bad_price('buy', initial_price):
                    await client.producer(messages.cancel_all_msg(client))
                    break
                else:
                    continue
        elif client.get_switch():
            initial_price = client.ticker.get_sell_price()
            await client.producer(messages.sell_msg(client, initial_price))
            while True:
                await client.producer(messages.order_status_msg(client))
                if client.get_order_state() == 'filled':
                    client.switch()
                    break
                elif client.ticker.bad_price('sell', initial_price):
                    await client.producer(messages.cancel_all_msg(client))
                    break
                else:
                    continue

async def main():
    client = Client()
    try:
        await trade_loop(client)
    except TypeError:
        print("Error occured, restarting")
        #cancel all orders, kill consumers & initialize new client
        await client.producer(messages.cancel_all_msg(client))
        await client.purge_consumers()
        new_client = Client()
        await trade_loop(new_client)

asyncio.run(main())