from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductResponse


router = APIRouter()


# -------------------------------------------------------------
# 1) 바코드로 제품 조회
# -------------------------------------------------------------
@router.get("/barcode/{barcode}", response_model=ProductResponse)
def get_product_by_barcode(barcode: str, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.barcode == barcode).first()

    if not product:
        raise HTTPException(status_code=404, detail="해당 바코드 제품을 찾을 수 없습니다.")

    return product


# -------------------------------------------------------------
# 2) 제품명 검색 기능  (LIKE 검색)
# -------------------------------------------------------------
@router.get("/search", response_model=list[ProductResponse])
def search_products(
    query: str = Query(..., description="제품명 검색어"),
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(Product.name.ilike(f"%{query}%"))
        .all()
    )

    if not products:
        raise HTTPException(status_code=404, detail="검색된 제품이 없습니다.")

    return products


# -------------------------------------------------------------
# 3) 단일 제품 상세조회 (ID 기준)
# -------------------------------------------------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product_detail(product_id: int, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다.")

    return product