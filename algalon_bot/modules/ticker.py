import asyncio
import websockets
import json
from algalon_bot.modules.messages.messages import ticker_msg
import algalon_bot.settings as settings

class Ticker:
    def __init__(self, ws):
        self.mark_price = None
        self.ws = ws

    async def refresh_price(self):
        """
        Refreshes mark price of selected instrument. 
        Uses connection given by Client() and initialized
        when Ticker() is created.
        """
        await self.ws.send(json.dumps(ticker_msg()))
        response = json.loads(await self.ws.recv())
        self.mark_price = response['result']['mark_price']
    
    async def get_current_price(self):
        await self.refresh_price()
        return self.mark_price
    
    async def get_buy_price(self):
        current_price = await self.get_current_price()
        return current_price - (settings.GAP / 2)

    async def get_sell_price(self):
        current_price = await self.get_current_price()
        return current_price + settings.GAP
    
    async def bad_price(self, order_type, initial_price):
        if order_type == "buy":
            if await self.get_current_price() > initial_price + settings.GAP + settings.GAP_IGNORE:
                return True
        elif order_type == "sell":
            if await self.get_current_price() < initial_price - settings.GAP - settings.GAP_IGNORE:
                return True
        else:
            return False