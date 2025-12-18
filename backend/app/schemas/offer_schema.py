from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OfferBase(BaseModel):
    mall_name: str
    price: float
    currency: str = "COP"
    url: Optional[str] = None


class OfferCreate(OfferBase):
    product_id: int


class OfferResponse(OfferBase):
    id: int
    product_id: int
    created_at: datetime

    class Config:
        orm_mode = True
