from datetime import datetime
import pathlib
import yaml

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
path = base_dir.joinpath("config.yaml")

def get_config():
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def get_instrument_name(config):
    return config['exchange']['instrument_name']

def get_gap(config):
    return config['robot']['gap']

def get_gap_ignore(config):
    return config['robot']['gap_ignore']

def get_amount(config):
    return config['exchange']['amount']

def expired(client):
    now = datetime.utcnow().timestamp()
    return True if now > client.get_token_expire() else False