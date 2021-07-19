from sqlalchemy import Boolean, Column, Integer, BigInteger, Float, String
from algalon_bot.modules.db.session import Base

class Order(Base):
    __tablename__ = "order"

    order_id = Column(BigInteger, primary_key=True, index=True)
    order_direction = Column(String, nullable=False)
    price = Column(Float)
    filled = Column(Boolean, default=False)
    creation_timestamp = Column(BigInteger)
