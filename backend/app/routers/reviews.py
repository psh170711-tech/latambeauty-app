from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db import get_db
from app import models
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ---------------------------------------------------------
# 평균 평점 및 리뷰 개수 업데이트 함수
# ---------------------------------------------------------
def update_product_rating(product_id: int, db: Session):
    reviews = db.query(models.Review).filter(models.Review.product_id == product_id).all()

    if len(reviews) == 0:
        avg_rating = 0.0
        count_rating = 0
    else:
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)
        count_rating = len(reviews)

    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    product.rating_avg = avg_rating
    product.rating_count = count_rating

    db.commit()
    db.refresh(product)


# ---------------------------------------------------------
# 1. 특정 상품에 리뷰 생성
# ---------------------------------------------------------
@router.post("/product/{product_id}", response_model=ReviewResponse)
def create_review(product_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_review = models.Review(
        product_id=product_id,
        user=review.user,
        rating=review.rating,
        comment=review.comment
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # 🔥 리뷰 추가 후 제품 평점 자동 업데이트
    update_product_rating(product_id, db)

    return db_review


# ---------------------------------------------------------
# 2. 특정 상품의 모든 리뷰 조회 (최신순)
# ---------------------------------------------------------
@router.get("/product/{product_id}", response_model=list[ReviewResponse])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(models.Review)
        .filter(models.Review.product_id == product_id)
        .order_by(models.Review.created_at.desc())
        .all()
    )
    return reviews


# ---------------------------------------------------------
# 3. 리뷰 1개 조회
# ---------------------------------------------------------
@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


# ---------------------------------------------------------
# 4. 리뷰 수정
# ---------------------------------------------------------
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.user = data.user
    review.rating = data.rating
    review.comment = data.comment

    db.commit()
    db.refresh(review)

    # 리뷰 수정 시도 제품 평점 다시 계산
    update_product_rating(review.product_id, db)

    return review


# ---------------------------------------------------------
# 5. 리뷰 삭제
# ---------------------------------------------------------
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    product_id = review.product_id

    db.delete(review)
    db.commit()

    # 삭제 후 제품 평점 재계산
    update_product_rating(product_id, db)

    return {"message": "Review deleted successfully"}
