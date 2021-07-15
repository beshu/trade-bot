import asyncio
import websockets
import json
import algalon_bot.settings as settings
from algalon_bot.modules.api_manager import APIManager

class Client:
    def __init__(self):
        self.link = settings.API_LINK
        self.queue = asyncio.Queue()
        self.api_manager = APIManager()
        self.api_consumers = [asyncio.create_task(self.api_manager.consumer()) for _ in range(5)]

    async def producer(self, msg):
        await self.queue.put(msg)

    async def consumer(self):
        while True:
            msg = await self.queue.get()
            async with websockets.connect(self.link) as websocket:
                await websocket.send(json.dumps(msg))
                response = json.loads(await websocket.recv())
                print(response)
                await self.api_manager.producer(response)
                self.queue.task_done()

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

    


    






