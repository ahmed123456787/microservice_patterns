from aio_pika import connect_robust, Message
import json
from .settings import settings
import asyncio
from functools import partial
import logging

logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self):
        self.amqp_url = settings.RABBITMQ_BROKER_URL
        self.connection = None
        self.channel = None
        self._connected = False


    async def connect(self):
        """Initialize the RabbitMQ connection"""
        if not self._connected:
            self.connection = await connect_robust(
                self.amqp_url, 
                loop=asyncio.get_event_loop()
            )
            self.channel = await self.connection.channel()
            self._connected = True
            logger.info("✅ RabbitMQ connection established!")
        return self   
     

    async def event_producer(self, exchange_name: str, binding_key: str, message: dict) -> None:
        if not self._connected:
            await self.connect()
            
        # Declare exchange
        exchange = await self.channel.declare_exchange(
            exchange_name,
            type='topic',
            durable=True
        )

        payload = json.dumps(message)
        await exchange.publish(
            Message(
                body=payload.encode(),
                content_type='application/json',
            ),
            routing_key=binding_key,
        )
        logger.info("✅ Message published successfully!")


    async def consume_messages(self, event_store: str, event: str, queue_name: str, callback):
        if not self._connected:
            await self.connect()
            
        exchange = await self.channel.declare_exchange(
            event_store,
            type='topic',
            durable=True
        )
        
        queue = await self.channel.declare_queue(queue_name, auto_delete=False)
        await queue.bind(exchange, event)
        
        logger.info(f"Consumer ready for routing key: {event}")
        await queue.consume(partial(self._process_message, callback=callback))


    async def _process_message(self, message, callback):
        logger.info(f" Received message: {message.body.decode()}")
        async with message.process():
            await callback(message.body.decode())
            

    async def close(self):
        """Close the RabbitMQ connection"""
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            self._connected = False
            logger.info("✅ RabbitMQ connection closed!")


# Initialize RabbitMQ client
amqp_client = RabbitMQClient()