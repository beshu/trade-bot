from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    order_type: str
    price: float
    filled: bool
    creation_timestamp: int
