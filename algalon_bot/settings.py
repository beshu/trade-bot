import algalon_bot.modules.util.util as util

config = util.get_config()

GAP = util.get_gap(config)
GAP_IGNORE = util.get_gap_ignore(config)
CLIENT_ID = util.get_client_id(config)
CLIENT_SECRET = util.get_client_secret(config)
API_LINK = util.get_api_link(config)
INSTRUMENT_NAME = util.get_instrument_name(config)
AMOUNT = util.get_amount(config)
SQLALCHEMY_DATABASE_SYNC_URI = util.get_sync_db_uri(config)
SQLALCHEMY_DATABASE_ASYNC_URI = util.get_async_db_uri(config)