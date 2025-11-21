from abc import ABC, abstractmethod
import logging
import json
from .schema import OrderCreatedEvent
from .domain import get_customer, check_balanace, make_order_fullfilled, create_payment, reject_order
from .database import get_db_session
from .rabbitmq import amqp_client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class MessageHandler(ABC):
    @abstractmethod
    async def handle_message(self, message: dict):
        pass


class OrderCreatedHandler(MessageHandler):

    async def handle_message(self, message_body: str):
        logger.info(f"Processing order created message: {message_body}")
        
        # Parse the JSON message string
        message = json.loads(message_body)
        order_obj = OrderCreatedEvent(**message)
        
        
         # Use context manager for automatic session handling
        with get_db_session() as db:
            customer = get_customer(db=db, customer_id=message['customer_id'])
            
            if customer:
                has_sufficient_balance = check_balanace(
                    db=db, 
                    customer_id=order_obj.customer_id, 
                    amount=order_obj.total_price
                )
                if has_sufficient_balance:
                    order_obj = make_order_fullfilled(order=order_obj)
                    create_payment(
                        db=db,
                        customer_id=order_obj.customer_id,
                        order_id=order_obj.order_id,
                        amount=order_obj.total_price
                    )
                    await amqp_client.event_producer('EVENT','order.fulfilled', order_obj.dict())
                    logger.info(f"Order {order_obj.order_id} fulfilled for customer {order_obj.customer_id}")
                
                else:
                    order = reject_order(order_obj)
                    await amqp_client.event_producer('EVENT','order.rejected', order_obj.dict())
                    logger.info(f"Order {order_obj.order_id} rejected due to insufficient balance for customer {order_obj.customer_id}")