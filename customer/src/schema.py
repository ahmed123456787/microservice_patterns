from pydantic import BaseModel


class OrderCreatedEvent(BaseModel):
    order_id: int
    product_id: int
    customer_id: int
    quantity: int
    total_price: float
    status: str
    created_at: str


class OrderFulfilledEvent(BaseModel):
    order_id: str
    status: str = "FULFILLED"
    fulfilled_at: str

class OrderRejectedEvent(BaseModel):
    order_id: str
    status: str = "REJECTED"
    reason: str