# app/analysis.py

def analyze_ingredients(product):
    ingredients = product.get("ingredients", [])
    if not ingredients:
        return {
            "avg_safety": 0,
            "high_risk_count": 0,
            "low_evidence_count": 0
        }

    avg_safety = sum(i["safety_score"] for i in ingredients) / len(ingredients)
    high_risk_count = len([i for i in ingredients if i["safety_score"] < 60])
    low_evidence_count = len([i for i in ingredients if i["evidence_level"] != "Robust"])

    return {
        "avg_safety": round(avg_safety, 1),
        "high_risk_count": high_risk_count,
        "low_evidence_count": low_evidence_count
    }