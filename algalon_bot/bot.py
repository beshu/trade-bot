from algalon_bot.modules.client import Client
from algalon_bot.modules.db_manager import DbManager
from algalon_bot.modules.db import session
import algalon_bot.modules.messages.messages as messages
from algalon_bot.modules.db import schemas
import asyncio


async def make_order(client, order_direction, db_manager):
    if order_direction == 'buy':
        initial_price = client.ticker.get_buy_price()
        await client.producer(messages.buy_msg(client, initial_price))
    elif order_direction == 'sell':
        initial_price = client.ticker.get_sell_price()
        await client.producer(messages.sell_msg(client, initial_price))
    db_order = schemas.Order(
            order_id = client.get_order_id(),
            order_direction = client.get_order_direction(),
            price = client.get_order_price(),
            order_state = False,
            creation_timestamp = client.get_order_timestamp()
        )
    print(db_order)
    await db_manager.place_order(db_order)
    print(
        client.get_order_id(),
        client.get_order_direction(),
        client.get_order_price(),
        client.get_order_timestamp()
    )
    await asyncio.sleep(1)
    while True:
        await client.producer(messages.order_status_msg(client))
        if client.get_order_state() == 'filled':
            client.switch()
            await db_manager.update_order(
                order_id=client.get_order_id(),
                order=schemas.Order(
                    order_id = client.get_order_id(),
                    order_direction = client.get_order_direction(),
                    price = client.get_order_price(),
                    order_state = True,
                    creation_timestamp = client.get_order_timestamp()
                )
            )
            print(
                client.get_order_id(),
                client.get_order_direction(),
                client.get_order_price(),
                client.get_order_timestamp()
            )
            await asyncio.sleep(1)
            break
        elif client.ticker.bad_price(order_direction, initial_price):
            await client.producer(messages.cancel_all_msg(client))
            break
        else:
            continue

async def trade_loop(client, db_manager):
    await client.producer(messages.auth_msg()), 
    await client.producer(messages.heartbeat_msg())
    while True:
        print("Bot started")
        if not client.get_switch():
           await make_order(client, 'buy', db_manager) 
        elif client.get_switch():
            await make_order(client, 'sell', db_manager) 

async def main():
    client = Client()
    db_manager = DbManager(session.SessionLocal, session.engine, session.Base)
    await db_manager.create_table()
    await trade_loop(client, db_manager)
    """
    except TypeError:
        print("Error occured, restarting")
        #cancel all orders, kill consumers & initialize new client
        await client.producer(messages.cancel_all_msg(client))
        await client.purge_consumers()
        new_client = Client()
        new_client.set_switch(client)
        await trade_loop(new_client, db_manager)
    """
asyncio.run(main())