import asyncio

class APIManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.order = None
        self.order_state = None
        self.token = None
        self.switch = False

    async def producer(self, response):
        await self.queue.put(response)

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
            self.queue.task_done()

    
    


