from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import get_db
from app import models
from app.schemas.product import ProductCreate, ProductResponse


router = APIRouter(prefix="/products", tags=["Products"])


# ---------------------------------------------------------
# 1. CREATE PRODUCT
# ---------------------------------------------------------
@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(
        name=data.name,
        brand=data.brand,
        barcode=data.barcode,
        ingredients=data.ingredients,
        image_url=data.image_url,
        category=data.category,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# ---------------------------------------------------------
# 2. GET ALL PRODUCTS
# ---------------------------------------------------------
@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# ---------------------------------------------------------
# 3. GET PRODUCT BY ID
# ---------------------------------------------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# ---------------------------------------------------------
# 4. UPDATE PRODUCT
# ---------------------------------------------------------
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = data.name
    product.brand = data.brand
    product.barcode = data.barcode
    product.ingredients = data.ingredients
    product.image_url = data.image_url
    product.category = data.category

    db.commit()
    db.refresh(product)
    return product


# ---------------------------------------------------------
# 5. DELETE PRODUCT
# ---------------------------------------------------------
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}


# ---------------------------------------------------------
# 6. GET PRODUCT BY BARCODE
# ---------------------------------------------------------
@router.get("/barcode/{barcode}", response_model=Optional[ProductResponse])
def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.barcode == barcode).first()

    # ❗️MVP 핵심 포인트:
    # 404로 보내면 프론트에서 “등록하기” 흐름 못 만듦
    # 존재 여부를 프론트가 확인해야 한다.
    if not product:
        return None

    return product
