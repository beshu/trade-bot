from algalon_bot.modules.client import Client
from algalon_bot.modules.db_manager import DbManager
from algalon_bot.modules.db import session
from algalon_bot.modules.util.util import expired
import algalon_bot.modules.messages.messages as messages
import asyncio

async def make_order(client, db_manager, action):
    # Buy or sell depending on action argument
    if action == 'buy':
        initial_price = await client.ticker.get_buy_price()
        await client.send(messages.buy_msg(client, initial_price))
    elif action == 'sell':
        initial_price = await client.ticker.get_sell_price()
        await client.send(messages.sell_msg(client, initial_price))

    # Place order in database
    db_order = client.get_order()
    await db_manager.place_order(db_order)

    while True:
        # Entering endless loop, checking order status
        await client.send(messages.order_status_msg(client))
        if client.get_order_state() == 'filled':
            # Updating status of order in database and switching
            db_order = client.get_order()
            await db_manager.update_order(
                order=db_order,
                order_id=db_order.order_id
            )
            client.switch()
            break
        elif await client.ticker.bad_price(action, initial_price):
            # Removing order from database if price is bad, 
            # Cancelling all active orders
            await db_manager.remove_order(client.get_order_id())
            await client.send(messages.cancel_all_msg(client))
            break
        else:
            continue

async def trade_loop(client, db_manager):
    # Authorization
    await client.send(messages.auth_msg())

    while True:
        print("Bot started")
        if not client.get_switch():
           await make_order(client, db_manager, action='buy') 
        elif client.get_switch():
            await make_order(client, db_manager, action='sell')

        # Token refresh 
        if expired(client):
            client.set_token(client.get_refresh_token())
            await client.send(messages.auth_msg())

async def main():
    try:
        client = Client()
        db_manager = DbManager(session.SessionLocal, session.engine, session.Base)
        await client.connect()
        await db_manager.create_table()
        await trade_loop(client, db_manager)
    finally:
        await client.terminate()

asyncio.run(main())