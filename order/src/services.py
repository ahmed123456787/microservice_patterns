from sqlalchemy.orm import Session
from .models import Order
from .schema import OrderSchema
from .rabbitmq import RabbitMQClient
import logging

logger = logging.getLogger(__name__)

class OrderService:

    @staticmethod
    async def create_order(db: Session, order_data: OrderSchema, amqp_client: RabbitMQClient) -> Order:
        new_order = Order(**order_data.dict())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Prepare JSON-serializable message
        message_data = {
            "order_id": new_order.id,
            "customer_id": new_order.customer_id,
            "product_id": new_order.product_id,
            "quantity": new_order.quantity,
            "total_price": new_order.total_price,
            "status": new_order.status.value,  # Convert enum to string
            "created_at": new_order.created_at.isoformat() if new_order.created_at else None
        }

        try:
            # Produce the message (order created) to RabbitMQ
            await amqp_client.event_producer("EVENT", "order.created", message_data)
            logger.info(f"✅ Order created event published for order {new_order.id}")
        except Exception as e:
            logger.error(f"❌ Failed to publish order created event: {e}")

        return new_order
    
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Order).offset(skip).limit(limit).all()

    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        return db.query(Order).filter(Order.id == order_id).first()

    @staticmethod
    def delete_order(db: Session, order_id: int) -> None:
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            db.delete(order)
            db.commit()
            return order
        return None