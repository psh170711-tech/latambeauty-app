// src/pages/Home.js
import Header from "../components/header/Header";
import BottomNav from "../components/layout/BottomNav";
import ProductCard from "../components/ProductCard";

const titleStyle = {
  fontSize: 18,
  fontWeight: 600,
  marginBottom: 12,
};

const labelStyle = {
  fontSize: 13,
  opacity: 0.7,
  marginBottom: 8,
};

const chipStyle = {
  padding: "10px 12px",
  borderRadius: 12,
  border: "1px solid rgba(255,255,255,0.08)",
  textAlign: "center",
  cursor: "pointer",
};

function Chip({ label }) {
  return <div style={chipStyle}>{label}</div>;
}

function CategoryRow({ title, items, columns = 4 }) {
  return (
    <div style={{ marginBottom: 20 }}>
      <div style={labelStyle}>{title}</div>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gap: 8,
        }}
      >
        {items.map((i) => (
          <Chip key={i} label={i} />
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <>
      {/* 🔥 Header가 검색을 전부 관리 */}
      <Header />

      <div style={{ padding: "16px 16px 100px" }}>
        {/* Skin Profile */}
        <section style={{ marginTop: 24 }}>
          <h3 style={titleStyle}>
            Real-time Popular Products by Skin Profile
          </h3>

          <CategoryRow
            title="Ethnicity"
            items={["LatAm", "White", "Black", "Asian"]}
          />

          <CategoryRow
            title="Country"
            items={[
              "🇧🇷 Brazil",
              "🇲🇽 Mexico",
              "🌎 Central America",
              "🇨🇴 Colombia",
              "🇦🇷 Argentina",
              "🇵🇪 Peru",
              "🇨🇱 Chile",
              "🇪🇨 Ecuador",
            ]}
          />

          <CategoryRow title="Age" items={["10s", "20s", "30s", "40s+"]} />

          <CategoryRow
            title="Gender"
            items={["Male", "Female", "Unisex"]}
            columns={3}
          />
        </section>

        {/* Products */}
        <section style={{ marginTop: 32 }}>
          <h3 style={titleStyle}>Real-time Popular Products</h3>

          <ProductCard
            product={{
              id: 1,
              brand: "Beauty of Joseon",
              name: "Relief Sun : Rice + Probiotics",
              price: 15900,
              risk: "LOW",
              safety: 84,
            }}
          />

          <ProductCard
            product={{
              id: 2,
              brand: "Round Lab",
              name: "1025 Dokdo Toner",
              price: 12800,
              risk: "MID",
              safety: 72,
            }}
          />

          <ProductCard
            product={{
              id: 3,
              brand: "COSRX",
              name: "Advanced Snail 96 Mucin Essence",
              price: 16500,
              risk: "LOW",
              safety: 79,
            }}
          />
        </section>
      </div>

      <BottomNav />
    </>
  );
}