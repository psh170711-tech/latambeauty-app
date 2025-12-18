from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=True)
    barcode = Column(String, unique=True, index=True)
    
    ingredients = Column(String, nullable=True)  # 🔥 성분 등록
    ingredient_score = Column(Float, nullable=True)  # 🔥 AI 점수
    safety_rating = Column(Float, nullable=True)  # 🔥 안전 점수
    risk_level = Column(String, nullable=True)  # 🔥 위험 레벨
    category = Column(String, nullable=True)  # 🔥 카테고리
    
    # Offer 관계 (가격 비교)
    offers = relationship("Offer", back_populates="product")