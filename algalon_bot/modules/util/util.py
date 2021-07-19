import pathlib
import yaml

base_dir = pathlib.Path(__file__).resolve().parent.parent.parent
path = base_dir.joinpath("config.yaml")

def get_config():
    with open(path) as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def get_instrument_name(config):
    return config['exchange']['instrument_name']

def get_client_id(config):
    return config['exchange']['client_id']

def get_client_secret(config):
    return config['exchange']['client_secret']

def get_api_link(config):
    return config['exchange']['api_link']

def get_gap(config):
    return config['robot']['gap']

def get_gap_ignore(config):
    return config['robot']['gap_ignore']

def get_amount(config):
    return config['exchange']['amount']

def get_sync_db_uri(config):
    return config['db']['sync_uri']

def get_async_db_uri(config):
    return config['db']['async_uri']

