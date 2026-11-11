from operator import index
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends ,FastAPI
from models import product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to the Farhan Page!"

products = [
    product(id=1, name="Samsung Galaxy S21", description="Latest Samsung smartphone", price=1000.0, quantity=5),
    product(id=2, name="Apple iPhone 13", description="Latest Apple smartphone", price=1200.0, quantity=10),
    product(id=3, name="Google Pixel 6", description="Latest Google smartphone", price=900.0, quantity=8),
    product(id=4, name="OnePlus 9", description="Latest OnePlus smartphone", price=700.0, quantity=12),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()
    count=db.query(database_models.product).count()

    if count == 0:
        for product in products:
            db.add(database_models.product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products")
def get_product(db: Session = Depends(get_db)):

    db_products = db.query(database_models.product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == product_id).first()
    if db_product:
        return db_product
    return "Product not  found"

@app.post("/products")
def add_product(new_product: product, db: Session = Depends(get_db)):
    db.add(database_models.product(**new_product.model_dump()))
    db.commit()
    return new_product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == product_id).first()
    if not db_product:
        return {"error": "Product not found"}

    for key, value in updated_product.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.product).filter(database_models.product.id == product_id).first()
    if not db_product:
        return {"error": "Product not found"}

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}
