from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    barcode = Column(String, unique=True, index=True)

    # 🔥 확장된 필드들
    ingredients = Column(String)                    # 성분
    image_url = Column(String, nullable=True)       # 이미지
    category = Column(String, nullable=True)        # 카테고리

    rating_avg = Column(Float, default=0.0)         # 평균 평점
    rating_count = Column(Integer, default=0)       # 리뷰 수

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # 관계 설정
    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete"
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user = Column(String)
    rating = Column(Integer)
    comment = Column(String)

    # 🔥 리뷰 생성 시간
    created_at = Column(DateTime, default=datetime.utcnow)

    # 역참조
    product = relationship("Product", back_populates="reviews")
