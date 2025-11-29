from pydantic import BaseModel
from datetime import datetime

class ReviewBase(BaseModel):
    user: str
    rating: int
    comment: str

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    product_id: int
    created_at: datetime  # 🔥 반드시 추가

    class Config:
        orm_mode = True
