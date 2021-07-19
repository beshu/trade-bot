from sqlalchemy.sql.expression import update
from algalon_bot.modules.db.crud import update_order


def test_get_order(test_order):
    assert test_order is not None
    
def test_update_order(test_db, test_pydantic_order, test_order):
    update_data = test_pydantic_order.dict()
    for key, value in update_data.items():
        setattr(test_order, key, value)
        print(key, value)
    test_db.add(test_order)
    test_db.commit()
    test_db.refresh(test_order)

def test_get_order(test_db, test_order_model, test_order_id):
    object = test_db.get(test_order_model, test_order_id)
    assert object is not None