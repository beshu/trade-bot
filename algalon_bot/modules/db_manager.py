from algalon_bot.modules.db.crud import get_order, create_order, update_order
from algalon_bot.modules.db import schemas


class DbManager():
    def __init__(self, session):
        self.db = session()

