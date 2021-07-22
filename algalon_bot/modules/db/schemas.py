from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    order_direction: str
    price: float
    order_state: str
    creation_timestamp: int
