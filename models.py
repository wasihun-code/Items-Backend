from sqlalchemy import Column, Integer, String, Float
from database import Base


class Items(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement='auto')
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Float)
