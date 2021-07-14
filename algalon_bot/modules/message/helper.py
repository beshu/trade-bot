def auth_msg(params: dict):
    msg = {
        "jsonrpc" : "2.0",
        "id" : 9929,
        "method" : "public/auth",
        "params" : {
            "grant_type" : "client_credentials",
            "client_id" : params['client_id'],
            "client_secret" : params['client_secret']
            }
    }
    return msg

def buy_msg(params: dict):
    msg = {
        "jsonrpc" : "2.0",
        "id" : 5275,
        "method" : "private/buy",
        "params" : {
            "instrument_name" : params['instrument_name'],
            "amount" : params['amount'],
            "type" : "limit",
            "label" : "algo"
        }
    }
    return msg

def sell_msg(params: dict):
    msg = {
        "jsonrpc" : "2.0",
        "id" : 2148,
        "method" : "private/sell",
        "params" : {
            "instrument_name" : params['instrument_name'],
            "amount" : params['amount'],
            "type" : "limit",
        }
    }
    return msg

def cancel_all_msg(params: dict):
    msg = {
        "jsonrpc" : "2.0",
        "id" : 4122,
        "method" : "private/cancel_all_by_instrument",
        "params" : {
            "instrument_name" : params['instrument_name'],
            "type" : "all"
        }
    }
    return msg

def ticker_msg(params):
    msg = {
        "jsonrpc": "2.0",
        "id": 8106,
        "method": "public/ticker",
        "params": {
            "instrument_name": params['instrument_name'],
        }
    }
    return msg