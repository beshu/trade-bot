import websockets
import algalon_bot.settings as settings
import algalon_bot.modules.message.helper as hlp
import asyncio
import json

msg = hlp.cancel_all_msg(
    {
        'instrument_name': settings.INSTRUMENT_NAME,
    }
)

async def cancel():
    async with websockets.connect(settings.API_LINK) as websocket:
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        return response


asyncio.run(cancel())