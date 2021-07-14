from algalon_bot.modules.ticker import get_mark_price
from algalon_bot.modules.buy import buy
from algalon_bot.modules.sell import sell 
from algalon_bot.modules.cancel import cancel
from algalon_bot.modules.auth import auth
import algalon_bot.modules.message.helper as hlp
import algalon_bot.settings as settings
import asyncio

async def buy_order(bought_event, sold_event, buy_order_placed):
    await sold_event.wait()
    current_price = await get_mark_price()
    buy_price = current_price - (settings.GAP/2)
    print("BUYING.\nBuy price: {}\nCurrent price: {}".format(buy_price, current_price))
    if not buy_order_placed.is_set():
        await buy(buy_price)
        print("Order placed")
        buy_order_placed.set()
    if current_price:
        print("Bought! Now sell")
        #Triggering sell order
        bought_event.set()
        sold_event.clear()
        buy_order_placed.clear()
    elif current_price > buy_price + settings.GAP + settings.GAP_IGNORE:
        await cancel()
        buy_order_placed.clear()
        print("Cancelled")
    else:
        print("Still not bought")

async def sell_order(bought_event, sold_event, sell_order_placed):
    await bought_event.wait()
    current_price = await get_mark_price()
    sell_price = current_price + settings.GAP
    print("SELLING.\nSell price: {}\nCurrent price: {}".format(sell_price, current_price))
    if not sell_order_placed.is_set():
        await sell(sell_price)
        sell_order_placed.set()
    if current_price:
        print("Sold! Now buying")
        #Triggering buy order
        sold_event.set()
        bought_event.clear()
        sell_order_placed.clear()
        if current_price < sell_price - settings.GAP - settings.GAP_IGNORE:
            await cancel()
            sell_order_placed.clear()
            print("Cancelled")
    else:
        print("Still not sold")

async def forever():
    bought_event = asyncio.Event()
    sold_event = asyncio.Event()
    buy_order_placed = asyncio.Event()
    sell_order_placed = asyncio.Event()
    await auth()
    sold_event.set()
    while True:
        await buy_order(bought_event, sold_event, buy_order_placed),
        await asyncio.sleep(5)
        await sell_order(bought_event, sold_event, sell_order_placed)

async def main():
    bought_event = asyncio.Event()
    sold_event = asyncio.Event()
    buy_order_placed = asyncio.Event()
    sell_order_placed = asyncio.Event()
    buy_task = asyncio.create_task(buy_order(bought_event, sold_event, buy_order_placed))
    sell_task = asyncio.create_task(sell_order(bought_event, sold_event, sell_order_placed))
    await auth()
    sold_event.set() #first sold to start buy_task
    await asyncio.gather(
            asyncio.sleep(1),
            buy_order(bought_event, sold_event, buy_order_placed),
            sell_order(bought_event, sold_event, sell_order_placed)
        ) 

#asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(forever())