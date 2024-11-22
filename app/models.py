from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    price = Column(Float)
    timestamp = Column(Integer)
