from fastapi import FastAPI
from src.database import create_tables
from src.initialize_data import initilize_data
from src.rabbitmq import amqp_client
from src.message_handlers import OrderCreatedHandler
import logging
from src.database import get_db
from fastapi import Depends

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

 
async def lifespan(app: FastAPI):

    #create tables
    create_tables()

    #initialize data
    initilize_data(db=next(get_db()))

    logger.info(" Starting application...")
    await amqp_client.connect()
    app.state.amqp_client = amqp_client

    await amqp_client.consume_messages("EVENT", "order.created", "order_payment_queue", OrderCreatedHandler().handle_message) 

    yield

    # Shutdown: close RabbitMQ connection 
    await amqp_client.close()


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Order Service is running."}