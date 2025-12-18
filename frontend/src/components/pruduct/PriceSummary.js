import React from "react";

export default function ProductHero({ product, bestOffer }) {
  if (!product) return null;

  return (
    <section style={styles.wrapper}>
      {/* 이미지 */}
      <div style={styles.imageBox}>
        <img
          src={product.image_url || "/placeholder.png"}
          alt={product.name}
          style={styles.image}
        />
      </div>

      {/* 정보 */}
      <div style={styles.info}>
        <div style={styles.category}>
          {product.category || "Skincare"}
        </div>

        <h1 style={styles.name}>{product.name}</h1>

        <div style={styles.sub}>
          {product.brand} · {product.volume}
        </div>

        {/* 핵심 지표 (지금은 더미) */}
        <div style={styles.badges}>
          <span style={styles.badge}>Risk: TBD</span>
          <span style={styles.badge}>Safety: TBD</span>
        </div>

        {/* 가격 */}
        {bestOffer && (
          <div style={styles.priceBox}>
            <div style={styles.price}>{bestOffer.price.toLocaleString()}원</div>
            <div style={styles.platform}>
              최저가 · {bestOffer.mall_name}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

const styles = {
  wrapper: {
    display: "grid",
    gridTemplateColumns: "120px 1fr",
    gap: 16,
    padding: 16,
    borderRadius: 20,
    background: "rgba(0,0,0,0.35)",
    border: "1px solid rgba(255,255,255,0.08)",
  },
  imageBox: {
    width: 120,
    height: 120,
    borderRadius: 16,
    background: "#fff",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  image: {
    maxWidth: "90%",
    maxHeight: "90%",
    objectFit: "contain",
  },
  info: {
    display: "flex",
    flexDirection: "column",
    gap: 6,
  },
  category: {
    fontSize: 12,
    opacity: 0.7,
  },
  name: {
    fontSize: 20,
    fontWeight: 800,
    lineHeight: 1.2,
  },
  sub: {
    fontSize: 13,
    opacity: 0.8,
  },
  badges: {
    display: "flex",
    gap: 8,
    marginTop: 6,
  },
  badge: {
    fontSize: 12,
    padding: "4px 8px",
    borderRadius: 999,
    background: "rgba(255,255,255,0.08)",
  },
  priceBox: {
    marginTop: 10,
  },
  price: {
    fontSize: 22,
    fontWeight: 900,
  },
  platform: {
    fontSize: 12,
    opacity: 0.7,
  },
};