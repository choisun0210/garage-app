from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.types import JSON
from database import Base
import datetime

class Record(Base):
    __tablename__ = "records"
    id = Column(String, primary_key=True, index=True)
    date = Column(String)
    duedate = Column(String)
    status = Column(String)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    carmodel = Column(String)
    plate = Column(String)
    year = Column(String)
    mileage = Column(String)
    color = Column(String)
    vin = Column(String)
    work = Column(Text)
    tech = Column(String)
    parts = Column(JSON)
    total = Column(Float)
    pay = Column(String)
    paystatus = Column(String)
    memo = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
