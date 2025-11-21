from abc import ABC, abstractmethod


class MessageHandler(ABC):
    @abstractmethod
    async def handle_message(self, message: dict):
        pass



class OrderFulfilledHandler(MessageHandler):

    async def handle_message(self, message: dict):
        # Process the order fulfilled message
        order_id = message
        print(f"Order {order_id} has been fulfilled.")


class OrderRejectedHandler(MessageHandler):
    
    async def handle_message(self, message: dict):
        # Process the order rejected message
        # order_id = message.get("order_id")
        # reason = message.get("reason", "No reason provided")
        print(f"Order {message} has been rejected.")