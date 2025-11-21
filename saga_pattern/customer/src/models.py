from sqlalchemy import Column, Integer, String, Float
from .database import Base
from enum import Enum


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    balance = Column(Float, default=0.0)
    address = Column(String, nullable=True)


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default=PaymentStatus.PENDING.value)