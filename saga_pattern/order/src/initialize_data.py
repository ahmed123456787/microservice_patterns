from .database import SessionLocal
from .models import Product


 
def initilize_data():
    db = SessionLocal()
    
    try:
        # Create some products if none exist
        if db.query(Product).count() == 0:
            products = [
                Product(name="Laptop", price=1203.00, stock=10),
                Product(name="Smartphone", price=800.00, stock=20),
                Product(name="Headphones", price=150.00, stock=30),
            ]
            
            db.add_all(products)
            db.commit()
            print("Initial products created successfully")
        else:
            print("Products already exist, skipping initialization")
            
    except Exception as e:
        db.rollback()
        print(f"Error initializing data: {e}")
        raise
    finally:
        db.close()