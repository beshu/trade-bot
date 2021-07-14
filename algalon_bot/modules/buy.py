import algalon_bot.modules.message.helper as hlp
import algalon_bot.settings as settings
import websockets
import json

msg = hlp.buy_msg(
    {
        'instrument_name': settings.INSTRUMENT_NAME,
        'amount': settings.AMOUNT
    }
)

async def buy(price):
    async with websockets.connect(settings.API_LINK) as websocket:
        msg['price'] = price
        await websocket.send(json.dumps(msg))
        response = await websocket.recv()
        return response