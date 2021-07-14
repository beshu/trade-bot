import asyncio
import websockets
import json
import algalon_bot.settings as settings
import algalon_bot.modules.message.helper as hlp
from algalon_bot.modules.util.util import get_config, get_instrument_name, get_api_link

msg = hlp.ticker_msg(
    {
        'instrument_name': settings.INSTRUMENT_NAME
    }
)

async def ticker(msg):
    async with websockets.connect(settings.API_LINK) as websocket:
        await websocket.send(msg)
        response = await websocket.recv()
        return response

async def get_mark_price():
    response_str = await ticker(json.dumps(msg))
    response = json.loads(response_str)
    return response['result']['mark_price']

async def do_stuff_periodically(interval, periodic_function):
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(),
        )

#asyncio.run(do_stuff_periodically(5, get_mark_price))

#response = json.loads(asyncio.run(ticker(json.dumps(msg))))

