from algalon_bot.modules.client import Client
import algalon_bot.settings as settings
import algalon_bot.modules.messages.messages as messages
import asyncio

async def get_current_price():
    return await messages.get_mark_price(messages.ticker_msg())

async def get_buy_price():
    return await get_current_price() - (settings.GAP / 2)

async def get_sell_price():
    return await get_current_price() + settings.GAP

async def bad_price(order_type, initial_price):
    if order_type == "buy":
        if await get_current_price() > initial_price + settings.GAP + settings.GAP_IGNORE:
            return True
        else:
            return False
    elif order_type == "sell":
        if await get_current_price() < initial_price - settings.GAP - settings.GAP_IGNORE:
            return True
        else:
            return False

async def buy_order_msg(client, price):
    msg = messages.buy_msg()
    msg['params']['price'] = price
    msg['params']['access_token'] = client.get_token()
    return msg

async def sell_order_msg(client, price):
    msg = messages.sell_msg()
    msg['params']['price'] = price
    msg['params']['access_token'] = client.get_token()
    return msg

async def status_order_msg(client):
    msg = messages.order_status_msg()
    msg['params']['order_id'] = client.get_order_id()
    msg['params']['access_token'] = client.get_token()
    return msg

async def cancel_all_msg(client):
    msg = messages.cancel_all_msg()
    msg['params']['access_token'] = client.get_token()
    return msg

async def auth_msg():
    msg = messages.auth_msg()
    return msg

async def heart_msg():
    msg = messages.heartbeat_msg()
    return msg


async def main():
    client = Client()
    consumers = [asyncio.create_task(client.consumer())
                 for _ in range(10)]

    await asyncio.gather(client.producer(await auth_msg()), client.producer(await heart_msg()))
    print("Authorized, heartbeat instantiated")
    while True:
        print("Bot started")
        print("Switch is {}".format(client.get_switch()))
        if not client.get_switch():
            initial_price = await get_buy_price()
            await client.producer(await buy_order_msg(client, initial_price))
            print("Started buy producer")
            while True:
                await client.producer(await status_order_msg(client))
                print("Started status producer for buy")
                if client.get_order_state() == 'filled':
                    print("Successfully bought")
                    client.switch()
                    break
                elif await bad_price('buy', initial_price):
                    await client.producer(await cancel_all_msg(client))
                    print("Bad price for buy")
                    await asyncio.sleep(1)
                    break
                else:
                    continue
        elif client.get_switch():
            initial_price = await get_sell_price()
            await client.producer(await sell_order_msg(client, initial_price))
            print("Started sell producer")
            while True:
                await client.producer(await status_order_msg(client))
                print("Created status producer for sell")
                if client.get_order_state() == 'filled':
                    print("Successfully sold")
                    client.switch()
                    break
                elif await bad_price('sell', initial_price):
                    await client.producer(await cancel_all_msg(client))
                    print("Bad price for sell")
                    await asyncio.sleep(1)
                    break
                else:
                    continue

asyncio.run(main())