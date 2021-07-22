import algalon_bot.modules.util.util as util
import os

config = util.get_config()

#from config.yaml
GAP = util.get_gap(config)
GAP_IGNORE = util.get_gap_ignore(config)
INSTRUMENT_NAME = util.get_instrument_name(config)
AMOUNT = util.get_amount(config)

#from dotenv
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_LINK = os.getenv("API_LINK")
SQLALCHEMY_DATABASE_SYNC_URI = os.getenv("SYNC_URI")
SQLALCHEMY_DATABASE_ASYNC_URI = os.getenv("ASYNC_URI")