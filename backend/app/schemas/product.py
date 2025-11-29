from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.review import ReviewResponse

class ProductCreate(BaseModel):
    name: str
    brand: str
    barcode: str
    ingredients: str
    image_url: Optional[str] = None
    category: Optional[str] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    barcode: str
    ingredients: str
    image_url: Optional[str]
    category: Optional[str]
    rating_avg: float
    rating_count: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    reviews: List[ReviewResponse] = []

    class Config:
        orm_mode = True
