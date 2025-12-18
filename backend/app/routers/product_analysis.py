# app/routers/product_analysis.py

from fastapi import APIRouter, HTTPException
from app.analysis import analyze_ingredients
from app.product_data import get_product_info

router = APIRouter()


@router.get("/analyze/{barcode}")
def analyze_product(barcode: str):
    """
    1) 바코드 기반 제품 정보를 받음 (MVP mock)
    2) 성분 분석 수행
    3) 위험도 + 점수 + 추천 반환
    """

    # 1) 제품 정보 가져오기
    product = get_product_info(barcode)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    ingredients = product.get("ingredients", "")

    # 2) 분석 수행
    result = analyze_ingredients(ingredients)

    # 구조화된 결과
    return {
        "barcode": barcode,
        "name": product.get("name"),
        "brand": product.get("brand"),
        "ingredients": ingredients,
        "score": result.get("score"),
        "risk": result.get("risk"),
        "warnings": result.get("warnings"),
        "recommended_products": result.get("recommended_products", []),
    }