import websockets
import algalon_bot.settings as settings
import algalon_bot.modules.message.helper as hlp
import json

msg = hlp.auth_msg(
    {
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET
    }
)

async def auth():
    async with websockets.connect(settings.API_LINK) as websocket:
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        return response