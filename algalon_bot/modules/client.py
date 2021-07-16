import asyncio
import websockets
import json
import algalon_bot.settings as settings
from algalon_bot.modules.api_manager import APIManager
from algalon_bot.modules.ticker import Ticker

class Client:
    def __init__(self):
        self.link = settings.API_LINK
        self.queue = asyncio.Queue()
        self.api_manager = APIManager()
        self.ticker = Ticker()
        self.consumers = [asyncio.create_task(self.consumer()) for _ in range(10)]

    async def producer(self, msg):
        await self.queue.put(msg)
        await asyncio.sleep(1)

    async def consumer(self):
        while True:
            msg = await self.queue.get()
            async with websockets.connect(self.link) as websocket:
                await websocket.send(json.dumps(msg))
                response = json.loads(await websocket.recv())
                print(response)
                await self.api_manager.producer(response)
                self.queue.task_done()
    
    async def purge_consumers(self):
        await self.api_manager.purge_consumers()
        await self.ticker.purge_consumers()
        for c in self.consumers:
            c.cancel()

    def get_order_id(self):
        return self.api_manager.order['result']['order']['order_id']

    def get_token(self):
        return self.api_manager.token
    
    def get_order_state(self):
        return self.api_manager.order_state
    
    def get_switch(self):
        return self.api_manager.switch

    def switch(self):
        self.api_manager.switch = not self.get_switch()
    
    

    


    






