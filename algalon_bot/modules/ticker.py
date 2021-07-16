import asyncio
import websockets
import json
from algalon_bot.modules.messages.messages import ticker_msg
import algalon_bot.settings as settings

class Ticker:
    def __init__(self):
        self.link = settings.API_LINK
        self.queue = asyncio.Queue()
        self.ticker_consumers = [asyncio.create_task(self.consumer()) for _ in range(3)]
        self.ticker_producer = asyncio.create_task(self.producer())
        self.mark_price = None
        
    async def producer(self):
        while True:
            await self.queue.put(ticker_msg())
            await asyncio.sleep(1)

    async def consumer(self):
        while True:
            msg = await self.queue.get()
            async with websockets.connect(self.link) as websocket:
                await websocket.send(json.dumps(msg))
                response = json.loads(await websocket.recv())
                self.mark_price = response['result']['mark_price']
                self.queue.task_done()
    
    async def purge_consumers(self):
        for c in self.ticker_consumers:
            c.cancel()
    
    def get_current_price(self):
        return self.mark_price
    
    def get_buy_price(self):
        return self.get_current_price() - (settings.GAP / 2)

    def get_sell_price(self):
        return self.get_current_price() + settings.GAP
    
    def bad_price(self, order_type, initial_price):
        if order_type == "buy":
            if self.get_current_price() > initial_price + settings.GAP + settings.GAP_IGNORE:
                return True
            else:
                return False
        elif order_type == "sell":
            if self.get_current_price() < initial_price - settings.GAP - settings.GAP_IGNORE:
                return True
            else:
                return False