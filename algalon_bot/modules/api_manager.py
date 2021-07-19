import asyncio

class APIManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.api_consumers = [asyncio.create_task(self.consumer()) for _ in range(5)]
        self.order = None
        self.order_state = None
        self.token = None
        self.token_expires = None
        self.refresh_token = None
        self.switch = False

    async def producer(self, response):
        await self.queue.put(response)
        await asyncio.sleep(1)

    async def consumer(self):
        while True:
            response = await self.queue.get()
            #buy & sell
            if response['id'] == 5275 or response['id'] == 2148:
                self.order_state = None
                self.order = response
            #cancel all
            elif response['id'] == 4122:
                self.order = None
                self.order_state = None
            #order status
            elif response['id'] == 4316:
                self.order_state = response['result']['order_state']
            #auth
            elif response['id'] == 9929:
                self.token = response['result']['access_token']
                self.token_expires = response['result']['expires_in']
                self.refresh_token = response['result']['refresh_token']
            self.queue.task_done()

    async def purge_consumers(self):
        for c in self.api_consumers:
            c.cancel()
            print("api consumer purged")
    
    


