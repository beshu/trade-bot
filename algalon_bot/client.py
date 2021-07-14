import asyncio
import websockets
import json
import algalon_bot.settings as settings
import algalon_bot.modules.message.helper as hlp

class Client:
    def __init__(self):
        self.link = settings.API_LINK
    
    async def websocket(self):
        return await websockets.connect(self.link)
    

    
