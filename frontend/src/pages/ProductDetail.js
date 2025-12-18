import { useParams } from "react-router-dom";
import IngredientRiskPanel from "../components/IngredientRiskPanel";

export default function ProductDetail() {
  const { id } = useParams();

  // 지금은 더미
  const product = {
    id,
    brand: "Beauty of Joseon",
    name: "Relief Sun : Rice + Probiotics",
    price: 15900,
    safety: 84,
    risk: "LOW",
  };

  return (
    <div style={{ padding: 16 }}>
      <h2>{product.name}</h2>
      <p>{product.brand}</p>
      <h3>{product.price.toLocaleString()}원</h3>

      <IngredientRiskPanel
        riskScore={product.risk}
        safetyScore={product.safety}
      />

      <button style={{ marginTop: 24 }}>최저가로 구매하기</button>
    </div>
  );
}