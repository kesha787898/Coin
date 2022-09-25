from sqlalchemy import Column, DateTime, String
from sqlalchemy import Integer, Float
from datetime import datetime

# Todo можно использовать только значения из списка.Подумать как сделать
from consts import Base


class Order(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    price = Column(Float, primary_key=False)
    tradable_quantity = Column(Float, primary_key=False)
    asset = Column(String, primary_key=False)
    fiat = Column(String, primary_key=False)
    type = Column(String, primary_key=False)
