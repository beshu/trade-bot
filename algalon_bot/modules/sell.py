import websockets
import algalon_bot.settings as settings
import algalon_bot.modules.message.helper as hlp
import json

msg = hlp.sell_msg(
    {
        'instrument_name': settings.INSTRUMENT_NAME,
        'amount': settings.AMOUNT,

    }
)

async def sell(price):
    async with websockets.connect(settings.API_LINK) as websocket:
        msg['price'] = price
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        return response
