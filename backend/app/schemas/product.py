from pydantic import BaseModel
from typing import Optional, List
from app.schemas.offer import OfferResponse

class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    barcode: Optional[str] = None
    ingredients: Optional[str] = None
    ingredient_score: Optional[float] = None
    safety_rating: Optional[float] = None
    risk_level: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    offers: List[OfferResponse] = []  # 가격 리스트

    class Config:
        orm_mode = True