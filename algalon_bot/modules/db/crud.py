from algalon_bot.modules.db import models

async def get_order(db, order_id):
    db_order = await db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if not db_order:
        return None
    return db_order

async def create_order(db, order):
    db_order = models.Order(
        order_id = order.order_id,
        order_type=order.order_type,
        price=order.price,
        filled=order.order_state,
        creation_timestamp=order.creation_timestamp,
    )
    await db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def update_order(db, order_id):
    db_order = await get_order(db, order_id)
    if not db_order:
        return None
    update_data = db_order.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    await db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def delete_order(db, order_id):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    await db.delete(db_order)
    await db.commit(db_order)
    return db_order


