from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    barcode = Column(String, unique=True, index=True)

    # 리뷰들 관계 설정
    reviews = relationship("Review", back_populates="product", cascade="all, delete")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user = Column(String)
    rating = Column(Integer)
    comment = Column(String)

    # 역참조
    product = relationship("Product", back_populates="reviews")
