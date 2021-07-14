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

async def bad_price(order_type, order_msg):
    order_price = order_msg['params']['price']
    if order_type == "buy":
        if await get_current_price() > order_price + settings.GAP + settings.GAP_IGNORE:
            return True
        else:
            return False
    elif order_type == "sell":
        if await get_current_price() < order_price + settings.GAP + settings.GAP_IGNORE:
            return True
        else:
            return False

async def buy_order_msg():
    msg = messages.buy_msg()
    msg['params']['price'] = await get_buy_price()
    return msg

async def sell_order_msg():
    msg = messages.sell_msg()
    msg['params']['price'] = await get_sell_price()
    return msg

async def status_order_msg(client):
    order_id = await client.get_order_id()
    msg = messages.order_status_msg()
    msg['params']['order_id'] = order_id
    return msg

async def cancel_all_msg():
    msg = messages.cancel_all_msg()
    return msg

async def auth_msg():
    msg = messages.auth_msg()
    return msg

async def heart_msg():
    msg = messages.heartbeat_msg()
    return msg


async def main():
    client = Client()
    buy_msg = await buy_order_msg()
    sell_msg = await sell_order_msg()
    auth_producer = asyncio.create_task(client.producer(await auth_msg()))
    buy_producer = asyncio.create_task(client.producer(buy_msg))
    sell_producer = asyncio.create_task(client.producer(sell_msg))
    cancel_producer = asyncio.create_task(client.producer(await cancel_all_msg()))
    heartbeat_producer = asyncio.create_task(client.producer(await heart_msg()))
    consumers = [asyncio.create_task(client.consumer())
                 for _ in range(10)]

    await asyncio.gather(auth_producer, heartbeat_producer)
    print("Authorized, heartbeat instantiated")

    while True:
        print("Entering while-true loop lvl 1")
        await asyncio.sleep(5)
        if not client.order_list:
            await asyncio.gather(buy_producer)
            print("Started buy producer")
            while True:
                status_producer = asyncio.create_task(client.producer(await status_order_msg(client)))
                await asyncio.gather(status_producer)
                print("Started status producer for buy")
                if await client.get_order_status() == 'filled':
                    print("Successfully bought")
                    break
                elif await bad_price('buy', buy_msg):
                    await asyncio.gather(cancel_producer)
                    print("Bad price for buy")
                    break
                else:
                    continue
        else:
            continue
        if client.order_list:
            await asyncio.gather(sell_producer)
            print("Started sell producer")
            while True:
                status_producer = asyncio.create_task(client.producer(await status_order_msg(client)))
                await asyncio.gather(status_producer)
                print("Created status producer for sell")
                if await client.get_order_status() == 'filled':
                    print("Successfully sold")
                    break
                elif await bad_price('sell', sell_msg):
                    await asyncio.gather(cancel_producer)
                    print("Bad price for sell")
                    break
                else:
                    continue
        else:
            continue


asyncio.run(main())