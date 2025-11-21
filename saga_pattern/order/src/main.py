from fastapi import FastAPI
from .database import create_tables
from .rabbitmq import amqp_client
from .initialize_data import initilize_data
import logging
from src.controller.order_controller import router as order_router
from src.message_handlers import OrderFulfilledHandler, OrderRejectedHandler


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_order_payment(message_body: str):
    logger.info(f"🎯 PROCESSING ORDER PAYMENT: {message_body}")

 
async def lifespan(app: FastAPI):
    logger.info(" Starting application...")
    
    # Startup: Create database tables
    create_tables()

    # Initialize data
    initilize_data()
    
    await amqp_client.connect() 
    app.state.amqp_client = amqp_client
    
    #listen back to messages sending from the customuer service.
    await amqp_client.consume_messages("EVENT", "order.fulfilled", "order_fulfillment_queue", callback=OrderFulfilledHandler().handle_message) 
    await amqp_client.consume_messages("EVENT", "order.rejected", "order_rejection_queue", callback=OrderRejectedHandler().handle_message)


    
    yield


    # Close the Connection
    await amqp_client.close()



app = FastAPI(lifespan=lifespan)
app.include_router(order_router)

@app.get("/")
async def root():
    return {"message": "Order Service is running."}
