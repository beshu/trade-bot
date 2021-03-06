from algalon_bot.modules.db.crud import create_order, update_order, delete_order


class DbManager():
    def __init__(self, session, engine, base):
        self.db = session()
        self.engine = engine
        self.base = base

    async def create_table(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def place_order(self, order):
        async with self.db:
            await create_order(self.db, order)
    
    async def update_order(self, order, order_id):
        async with self.db:
            await update_order(self.db, order, order_id)
    
    async def remove_order(self, order_id):
        async with self.db:
            await delete_order(self.db, order_id)

