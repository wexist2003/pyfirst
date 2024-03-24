from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    birthday = Column(Date, index=True)
    created_at = Column(DateTime, default = func.now())
    updated_at = Column(DateTime, default = func.now(), onupdate = func.now())
