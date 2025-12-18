from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    seller_name = Column(String, nullable=True)  # 🔥 판매자 이름 추가
    price = Column(Float, nullable=False)
    currency = Column(String, default="COP")
    url = Column(String, nullable=True)
    shipping_fee = Column(Float, nullable=True)  # 🔥 배송비
    last_checked_at = Column(DateTime, default=datetime.utcnow)  # 🔥 최근 확인

    product = relationship("Product", back_populates="offers")