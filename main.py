from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Product(BaseModel):
    id: int
    name: str
    price: int

# Home
@app.get("/")
def store_description():
    return {"message": "Welcome To My Store"}

# Get all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(models.ProductDB).all()

# Create product
@app.post("/product")
def add_product(product: Product, db: Session = Depends(get_db)):
    existing = db.query(models.ProductDB).filter(models.ProductDB.id == product.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product ID already exists")

    new_product = models.ProductDB(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product created", "product": new_product}

# Update product
@app.put("/product/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    product = db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = updated_product.name
    product.price = updated_product.price

    db.commit()
    db.refresh(product)

    return {"message": "Updated", "product": product}

# Update price
@app.patch("/product/{product_id}/price")
def update_price(product_id: int, price: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.price = price
    db.commit()

    return {"message": "Price updated", "product": product}

# Delete product
@app.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.ProductDB).filter(models.ProductDB.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Deleted successfully"}