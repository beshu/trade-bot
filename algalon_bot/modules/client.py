import websockets
import json
import algalon_bot.settings as settings
from algalon_bot.modules.api_manager import APIManager
from algalon_bot.modules.ticker import Ticker
from algalon_bot.modules.db import schemas

class Client:
    def __init__(self):
        self.api_manager = APIManager()
        self.ws = None
        self.ticker = None
    
    async def connect(self):
        """
        Connect Client() and Ticker() to websocket. 
        """
        self.ws = await websockets.connect(settings.API_LINK)
        self.ticker = Ticker(self.ws)
    
    async def send(self, msg):
        """
        Sends msg to Deribit API through websocket and
        receives response, then gives it to APIManager()
        to store order parameteres, tokens etc. 

        Args:
            msg (str): String message coming from .messages module.
                       Will be serialized via json.dumps() and then
                       deserialized to process response.
        """
        await self.ws.send(json.dumps(msg))
        response = json.loads(await self.ws.recv())
        await self.api_manager.process_response(response)
        print(response)

    async def terminate(self):
        """
        Terminates connection to websocket, thus stops the bot.
        """
        await self.ws.close()
    
    def switch(self):
        """
        Reverse the APIManager().switch state in order to start
        buy or sell action depending on previous state. 
        """
        self.api_manager.switch = not self.get_switch()
    
    def get_order(self):
        """
        Creates pydantic model to validate data and use 
        it in DbManager() actions such as place_order(), 
        update_order() and remove_order()

        Returns:
            pydantic.BaseModel: model with needed attrs to
                                validate and perform CRUD 
                                actions
        """
        return schemas.Order(
                order_id = self.get_order_id(),
                order_direction = self.get_order_direction(),
                price = self.get_order_price(),
                order_state = self.get_order_state(),
                creation_timestamp = self.get_order_timestamp()
            )
    
    def get_switch(self):
        return self.api_manager.switch
    
    def get_order_price(self):
        return self.api_manager.order['result']['order']['price']
    
    def get_order_direction(self):
        return self.api_manager.order['result']['order']['direction']

    def get_order_id(self):
        return self.api_manager.order['result']['order']['order_id']
    
    def get_order_timestamp(self):
        return self.api_manager.order['result']['order']['creation_timestamp']
    
    def get_order_state(self):
        return self.api_manager.order_state

    def get_token(self):
        return self.api_manager.token
    
    def get_token_expire(self):
        return self.api_manager.token_expires
    
    def get_refresh_token(self):
        return self.api_manager.refresh_token

    def set_token(self, refresh_token):
        self.api_manager.token = refresh_token



    


    






