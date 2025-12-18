from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OfferResponse(BaseModel):
    id: int
    seller_name: Optional[str]
    price: float
    currency: str
    url: Optional[str]
    shipping_fee: Optional[float]
    last_checked_at: datetime

    class Config:
        orm_mode = True