from .models import Customer
from sqlalchemy.orm import Session

  

def initilize_data(db: Session):

    # Check if data already exists
    if db.query(Customer).first():
        return  # Data already initialized

    customers = [
        Customer(name="Alice",email="def@gmail.com",address="def", balance=100.0),  
    ]

    db.add_all(customers)
    db.commit()