from src.services import OrderService
from src.schema import OrderSchema, OrderResponse
from src.database import get_db
from fastapi import APIRouter, Depends
from src.rabbitmq import amqp_client


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse)
async def create_order(order_data: OrderSchema, db=Depends(get_db)):
    order = await OrderService.create_order(db, order_data, amqp_client)
    return order
