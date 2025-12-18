from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.review import Review
from app.models.product import Product
from app.schemas.review import ReviewCreate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ---------------------------------------------------------
# ⭐ 제품 평점 자동 업데이트 함수
# ---------------------------------------------------------
def update_product_rating(product_id: int, db: Session):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()

    if len(reviews) == 0:
        avg_rating = 0.0
        count_rating = 0
    else:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        count_rating = len(reviews)

    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.rating_avg = avg_rating
        product.rating_count = count_rating
        db.commit()
        db.refresh(product)


# ---------------------------------------------------------
# 1️⃣ 특정 제품에 리뷰 생성
# ---------------------------------------------------------
@router.post("/product/{product_id}", response_model=ReviewResponse)
def create_review(product_id: int, review: ReviewCreate, db: Session = Depends(get_db)):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_review = Review(
        product_id=product_id,
        user=review.user,
        rating=review.rating,
        comment=review.comment,
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # 리뷰 생성 후 평점 업데이트
    update_product_rating(product_id, db)

    return db_review


# ---------------------------------------------------------
# 2️⃣ 특정 제품의 리뷰 목록 조회 (최신순)
# ---------------------------------------------------------
@router.get("/product/{product_id}", response_model=list[ReviewResponse])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.product_id == product_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return reviews


# ---------------------------------------------------------
# 3️⃣ 리뷰 1개 조회
# ---------------------------------------------------------
@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


# ---------------------------------------------------------
# 4️⃣ 리뷰 수정
# ---------------------------------------------------------
@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewCreate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    review.user = data.user
    review.rating = data.rating
    review.comment = data.comment

    db.commit()
    db.refresh(review)

    # 리뷰 수정 후 평점 업데이트
    update_product_rating(review.product_id, db)

    return review


# ---------------------------------------------------------
# 5️⃣ 리뷰 삭제
# ---------------------------------------------------------
@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    product_id = review.product_id

    db.delete(review)
    db.commit()

    # 리뷰 삭제 후 평점 업데이트
    update_product_rating(product_id, db)

    return {"message": "Review deleted successfully"}