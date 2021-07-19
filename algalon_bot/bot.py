from algalon_bot.modules.client import Client
from algalon_bot.modules.db_manager import DbManager
from algalon_bot.modules.db import session
import algalon_bot.modules.messages.messages as messages
from algalon_bot.modules.db import schemas
import asyncio
from datetime import datetime

def expired(client):
    now = datetime.utcnow().timestamp()
    return True if now > (now - 10) + client.get_token_expire() else None

def get_order(client, state):
    return schemas.Order(
            order_id = client.get_order_id(),
            order_direction = client.get_order_direction(),
            price = client.get_order_price(),
            order_state = state,
            creation_timestamp = client.get_order_timestamp()
        )

async def make_order(client, order_direction, db_manager):
    if order_direction == 'buy':
        initial_price = client.ticker.get_buy_price()
        await client.producer(messages.buy_msg(client, initial_price))
    elif order_direction == 'sell':
        initial_price = client.ticker.get_sell_price()
        await client.producer(messages.sell_msg(client, initial_price))
    db_order = get_order(client, False)
    await db_manager.place_order(db_order)
    while True:
        await client.producer(messages.order_status_msg(client))
        if client.get_order_state() == 'filled':
            db_order = get_order(client, True)
            await db_manager.update_order(
                order=db_order,
                order_id=client.get_order_id()
            )
            client.switch()
            break
        elif client.ticker.bad_price(order_direction, initial_price):
            await db_manager.remove_order(client.get_order_id())
            await client.producer(messages.cancel_all_msg(client))
            break
        else:
            continue

async def trade_loop(client, db_manager):
    await client.producer(messages.auth_msg())
    while True:
        print("Bot started")
        if not client.get_switch():
           await make_order(client, 'buy', db_manager) 
        elif client.get_switch():
            await make_order(client, 'sell', db_manager) 
        if expired(client):
            client.set_token(client.get_refresh_token())
            await client.producer(messages.auth_msg())

async def main():
    client = Client()
    db_manager = DbManager(session.SessionLocal, session.engine, session.Base)
    await db_manager.create_table()
    await trade_loop(client, db_manager)

asyncio.run(main())