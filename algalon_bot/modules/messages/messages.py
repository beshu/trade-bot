import algalon_bot.settings as settings
import websockets
import json

def ticker_msg():
    msg = {
        "jsonrpc": "2.0",
        "id": 8106,
        "method": "public/ticker",
        "params": {
            "instrument_name": settings.INSTRUMENT_NAME,
        }
    }
    return msg

def auth_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 9929,
        "method" : "public/auth",
        "params" : {
            "grant_type" : "client_credentials",
            "client_id" : settings.CLIENT_ID,
            "client_secret" : settings.CLIENT_SECRET
            }
    }
    return msg

def buy_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 5275,
        "method" : "private/buy",
        "params" : {
            "instrument_name" : settings.INSTRUMENT_NAME,
            "amount" : settings.AMOUNT,
            "type" : "limit",
            "label" : "algo",
        }
    }
    return msg

def sell_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 2148,
        "method" : "private/sell",
        "params" : {
            "instrument_name" : settings.INSTRUMENT_NAME,
            "amount" : settings.AMOUNT,
            "type" : "limit",
        }
    }
    return msg

def cancel_all_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 4122,
        "method" : "private/cancel_all_by_instrument",
        "params" : {
            "instrument_name" : settings.INSTRUMENT_NAME,
            "type" : "all"
        }
    }
    return msg

def order_status_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 4316,
        "method" : "private/get_order_state",
        "params" : {
        }
    }
    return msg

def heartbeat_msg():
    msg = {
        "jsonrpc" : "2.0",
        "id" : 9098,
        "method" : "public/set_heartbeat",
        "params" : {
            "interval" : 30
        }
    }
    return msg

async def ticker(msg):
    async with websockets.connect(settings.API_LINK) as websocket:
        await websocket.send(msg)
        response = await websocket.recv()
        return response

async def get_mark_price(msg):
    response_str = await ticker(json.dumps(msg))
    response = json.loads(response_str)
    return response['result']['mark_price']