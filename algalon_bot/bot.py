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
    msg['params']['access_token'] = client.token
    return msg

async def cancel_all_msg(client):
    msg = messages.cancel_all_msg()
    msg['params']['access_token'] = client.token
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
    #auth_producer = asyncio.create_task(client.producer(await auth_msg()))
    #buy_producer = asyncio.create_task(client.producer(buy_msg))
    #sell_producer = asyncio.create_task(client.producer(sell_msg))
    #cancel_producer = asyncio.create_task(client.producer(await cancel_all_msg()))
    #heartbeat_producer = asyncio.create_task(client.producer(await heart_msg()))
    consumers = [asyncio.create_task(client.consumer())
                 for _ in range(10)]

    print("Hello")
    await asyncio.gather(client.producer(await auth_msg()), client.producer(await heart_msg()))
    print("Authorized, heartbeat instantiated")

    while True:
        print("Entering while-true loop lvl 1")
        await asyncio.sleep(5)
        print(client.order_list)
        if len(client.order_list) == 0:
            buy_msg['params']['access_token'] = client.token
            await client.producer(buy_msg)
            print("Started buy producer")
            while True:
                status_msg = await status_order_msg(client)
                await client.producer(status_msg)
                print("Started status producer for buy")
                if client.order_status == 'filled':
                    print("Successfully bought")
                    break
                elif await bad_price('buy', buy_msg):
                    await client.producer(await cancel_all_msg(client))
                    print("Bad price for buy")
                    break
                else:
                    continue
        else:
            continue
        if client.order_list:
            client.clear_all()
            sell_msg['params']['access_token'] = client.token
            await client.producer(sell_msg)
            print("Started sell producer")
            while True:
                await client.producer(await status_order_msg(client))
                print("Created status producer for sell")
                if client.order_status == 'filled':
                    print("Successfully sold")
                    client.clear_all()
                    break
                elif await bad_price('sell', sell_msg):
                    await client.producer(await cancel_all_msg(client))
                    print("Bad price for sell")
                    break
                else:
                    continue
        else:
            continue


asyncio.run(main())