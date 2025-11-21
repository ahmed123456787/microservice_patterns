from .models import Customer, Payment, PaymentStatus
from sqlalchemy.orm import Session


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def check_balanace(db: Session, customer_id: int, amount: float) -> bool:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer and customer.balance >= amount:
        return True
    return False


def make_order_fullfilled(order:dict):
    order.status = "FULFILLED"
    return order

def reject_order(order:dict):
    order.status = "REJECTED"
    return order


def create_payment(db: Session, customer_id: int, order_id: int, amount: float):

    payment = Payment(
        customer_id=customer_id,
        order_id=order_id,
        amount=amount,
        status=PaymentStatus.COMPLETED.value
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment