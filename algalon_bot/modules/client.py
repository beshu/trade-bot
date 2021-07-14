import asyncio
import websockets
import json
import algalon_bot.settings as settings

class Client:
    def __init__(self):
        self.link = settings.API_LINK
        self.queue = asyncio.Queue()
        self.order_list = []
        self.status_list = []

    def clear(self):
        self.order_list.clear()
        self.status_list.clear()

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
                if response['id'] == 5275 or 2148:
                    self.order_list.append(response)
                elif response['id'] == 4122:
                    self.clear()
                elif response['id'] == 4316:
                    self.status_list.append(response)
                self.queue.task_done()

    async def get_order_id(self):
        print(self.order_list)
        return await self.order_list[0]['result']['order']['order_id']

    async def get_order_status(self):
        return await self.status_list[0]['result']['order_state']


    






