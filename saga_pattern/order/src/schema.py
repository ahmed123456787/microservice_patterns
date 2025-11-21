from pydantic import BaseModel
from .models import OrderStatus
from datetime import datetime
from typing import Optional

class OrderSchema(BaseModel):
    customer_id: int
    product_id: int
    status: OrderStatus
    quantity: int
    total_price: float

    class Config:
        orm_mode = True


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    product_id: int
    status: OrderStatus
    quantity: int
    total_price: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True