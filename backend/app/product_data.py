# app/product_data.py

products = [
    {
        "barcode": "8809643061234",
        "name": "Example Hydrating Cream",
        "brand": "BrandX",
        "image_url": "https://example.com/product.jpg",
        "ingredients": [
            {
                "name": "Glycerin",
                "role": "Humectant",
                "safety_score": 95,
                "evidence_level": "Robust",
                "issues": [],
                "description": "피부에 수분을 끌어당겨 보습력을 높여주는 성분."
            },
            {
                "name": "Butylene Glycol",
                "role": "Solvent",
                "safety_score": 85,
                "evidence_level": "Robust",
                "issues": [],
                "description": "보습 및 흡수력 개선에 도움."
            },
            {
                "name": "Fragrance",
                "role": "Fragrance",
                "safety_score": 40,
                "evidence_level": "Limited",
                "issues": ["Irritation", "Allergy Risk"],
                "description": "향료로 민감성 피부엔 자극이 될 수 있음."
            }
        ],
        "recommended_products": ["8809643065678"]
    },
    {
        "barcode": "8809643065678",
        "name": "Mild Cream Edition",
        "brand": "BrandX",
        "image_url": "https://example.com/mild.jpg",
        "ingredients": [
            {
                "name": "Glycerin",
                "role": "Humectant",
                "safety_score": 95,
                "evidence_level": "Robust",
                "issues": [],
                "description": "피부 보습 제공."
            }
        ],
        "recommended_products": []
    }
]

def get_product_by_barcode(barcode: str):
    for p in products:
        if p["barcode"] == barcode:
            return p
    return None