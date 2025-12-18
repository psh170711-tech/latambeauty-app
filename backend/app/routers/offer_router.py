from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.offer import Offer
from app.schemas.offer import OfferResponse

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.get("/product/{product_id}", response_model=List[OfferResponse])
def get_offers(product_id: int, db: Session = Depends(get_db)):
    offers = db.query(Offer).filter(Offer.product_id == product_id).all()
    return offers