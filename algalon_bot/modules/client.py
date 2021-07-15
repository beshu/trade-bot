import asyncio
import websockets
import json
import algalon_bot.settings as settings

class Client:
    def __init__(self):
        self.link = settings.API_LINK
        self.queue = asyncio.Queue()
        self.order_list = []
        self.order_status = None
        self.token = None

    def clear_all(self):
        self.order_list.clear()
        self.status = None

    async def producer(self, msg):
        await self.queue.put(msg)
        await asyncio.sleep(1)

    async def consumer(self):
        while True:
            msg = await self.queue.get()
            print("Retreived from queue")
            async with websockets.connect(self.link) as websocket:
                await websocket.send(json.dumps(msg))
                response = json.loads(await websocket.recv())
                print(response)
                if response['id'] == 5275 or response['id'] == 2148:
                    self.order_list.append(response)
                elif response['id'] == 4122:
                    self.clear_all()
                elif response['id'] == 4316:
                    self.order_status = response['result']['order_state']
                elif response['id'] == 9929:
                    self.token = response['result']['access_token']
                self.queue.task_done()

    async def get_order_id(self):
        return self.order_list[0]['result']['order']['order_id']

    


    






