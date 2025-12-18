import { useNavigate } from "react-router-dom";

export default function ProductCard({ product }) {
  const navigate = useNavigate();

  return (
    <div
      onClick={() => navigate(`/product/${product.id}`)}
      style={{
        display: "flex",
        gap: 12,
        padding: 14,
        borderRadius: 16,
        border: "1px solid rgba(255,255,255,0.08)",
        cursor: "pointer",
      }}
    >
      <div
        style={{
          width: 56,
          height: 56,
          borderRadius: 12,
          background: "#222",
        }}
      />
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 12, opacity: 0.6 }}>{product.brand}</div>
        <div style={{ fontWeight: 600 }}>{product.name}</div>
        <div style={{ fontSize: 12, marginTop: 4 }}>
          Risk: {product.risk} · Safety: {product.safety}
        </div>
      </div>
      <div style={{ fontWeight: 600 }}>
        {product.price.toLocaleString()}원
      </div>
    </div>
  );
}