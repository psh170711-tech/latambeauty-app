#!/bin/zsh

BASE_DIR="$HOME/latambeauty-app/frontend/src"

echo ""
echo "====================================================="
echo "🔥 LatamBeauty 프론트엔드 구조 재정리 스크립트 시작!"
echo "====================================================="
echo ""
read "ok?👉 ENTER 를 누르면 시작합니다. "

#######################################################
# STEP 1 — 디렉토리 확인 및 생성
#######################################################

echo ""
echo "📂 STEP 1) 프로젝트 경로 확인"
echo "   BASE_DIR = $BASE_DIR"
sleep 1

if [ ! -d "$BASE_DIR" ]; then
  echo "❌ 오류: $BASE_DIR 디렉토리가 존재하지 않습니다."
  exit 1
else
  echo "✅ 경로 정상 확인됨!"
fi

echo ""
echo "📁 STEP 1-2) 필요한 디렉토리 생성(api, components, pages, styles)..."
sleep 1

mkdir -p "$BASE_DIR/api"
mkdir -p "$BASE_DIR/components"
mkdir -p "$BASE_DIR/pages"
mkdir -p "$BASE_DIR/styles"

echo "➡️ 생성 완료!"
read "ok?👉 다음 단계로 가려면 ENTER "



#######################################################
# STEP 2 — API 파일 생성
#######################################################

echo ""
echo "====================================================="
echo "🧩 STEP 2) API 모듈 생성 (productApi.js, priceApi.js)"
echo "====================================================="
sleep 1


################################
# productApi.js
################################
cat << 'EOF' > "$BASE_DIR/api/productApi.js"
import axios from "axios";

// 나중에 .env 로 분리 가능
const API_BASE_URL = "http://127.0.0.1:8000";

export async function fetchProductByBarcode(barcode) {
  if (!barcode || !barcode.trim()) {
    throw new Error("바코드를 입력해주세요.");
  }

  try {
    const response = await axios.get(
      `${API_BASE_URL}/products/barcode/${encodeURIComponent(barcode.trim())}`
    );
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("제품 조회 중 오류가 발생했습니다.");
  }
}
EOF


################################
# priceApi.js
################################
cat << 'EOF' > "$BASE_DIR/api/priceApi.js"
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * 가격비교용 API
 */
export async function fetchPricesByProductId(productId) {
  if (!productId) {
    throw new Error("productId 가 없습니다.");
  }

  try {
    const response = await axios.get(
      `${API_BASE_URL}/prices/product/${encodeURIComponent(productId)}`
    );
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("가격 정보를 불러오지 못했습니다.");
  }
}
EOF

echo "✅ API 모듈 생성 완료!"
read "ok?👉 다음 단계로 가려면 ENTER "



#######################################################
# STEP 3 — Components 생성
#######################################################

echo ""
echo "====================================================="
echo "🧱 STEP 3) Components 생성(SearchBar, ProductCard 등)"
echo "====================================================="
sleep 1


################################
# SearchBar.js
################################
cat << 'EOF' > "$BASE_DIR/components/SearchBar.js"
import React from "react";

const SearchBar = ({ value, onChange, onSubmit }) => {
  const handleKeyDown = (e) => {
    if (e.key === "Enter") onSubmit();
  };

  return (
    <div style={{ display: "flex", gap: "8px", marginBottom: "24px" }}>
      <input
        type="text"
        placeholder="바코드를 입력하세요"
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        style={{
          flex: 1,
          padding: "12px 16px",
          borderRadius: "8px",
          border: "1px solid #ddd",
          fontSize: "16px",
        }}
      />
      <button
        onClick={onSubmit}
        style={{
          minWidth: "96px",
          padding: "12px 16px",
          borderRadius: "8px",
          border: "none",
          backgroundColor: "#111827",
          color: "white",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        조회
      </button>
    </div>
  );
};

export default SearchBar;
EOF



################################
# ProductCard.js
################################
cat << 'EOF' > "$BASE_DIR/components/ProductCard.js"
import React from "react";

const ProductCard = ({ product }) => {
  if (!product) return null;

  const {
    name,
    brand,
    image_url,
    ingredient_score,
    safety_rating,
    risk_level,
  } = product;

  return (
    <div
      style={{
        borderRadius: "16px",
        border: "1px solid #e5e7eb",
        padding: "24px",
        display: "flex",
        gap: "24px",
        marginBottom: "24px",
      }}
    >
      {image_url && (
        <div
          style={{
            width: "140px",
            height: "140px",
            borderRadius: "16px",
            overflow: "hidden",
            backgroundColor: "#f9fafb",
            flexShrink: 0,
          }}
        >
          <img
            src={image_url}
            alt={name}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </div>
      )}

      <div style={{ flex: 1 }}>
        <h2 style={{ fontSize: "24px", marginBottom: "4px" }}>{name}</h2>
        {brand && (
          <p style={{ color: "#6b7280", marginBottom: "12px" }}>브랜드: {brand}</p>
        )}

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: "12px",
            fontSize: "14px",
          }}
        >
          {ingredient_score !== undefined && (
            <span
              style={{
                padding: "6px 10px",
                borderRadius: "999px",
                backgroundColor: "#eef2ff",
                color: "#3730a3",
              }}
            >
              성분 점수: {ingredient_score}
            </span>
          )}

          {safety_rating !== undefined && (
            <span
              style={{
                padding: "6px 10px",
                borderRadius: "999px",
                backgroundColor: "#ecfdf3",
                color: "#15803d",
              }}
            >
              안전도: {safety_rating}/5
            </span>
          )}

          {risk_level && (
            <span
              style={{
                padding: "6px 10px",
                borderRadius: "999px",
                backgroundColor: "#fef2f2",
                color: "#b91c1c",
              }}
            >
              위험도: {risk_level}
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;
EOF



################################
# PriceTable.js
################################
cat << 'EOF' > "$BASE_DIR/components/PriceTable.js"
import React from "react";

const PriceTable = ({ prices }) => {
  if (!prices || prices.length === 0) {
    return (
      <p style={{ color: "#6b7280", marginTop: "8px" }}>
        아직 등록된 가격 정보가 없습니다.
      </p>
    );
  }

  const sorted = [...prices].sort((a, b) => a.price - b.price);
  const min = sorted[0].price;

  return (
    <div style={{ marginTop: "8px" }}>
      <h3 style={{ fontSize: "18px", marginBottom: "8px" }}>가격 비교</h3>

      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr style={{ backgroundColor: "#f9fafb" }}>
            <th style="padding:8px;text-align:left;">쇼핑몰</th>
            <th style="padding:8px;text-align:right;">가격</th>
            <th style="padding:8px;text-align:center;">링크</th>
          </tr>
        </thead>

        <tbody>
          {sorted.map((item, idx) => (
            <tr key={idx}>
              <td style={{ padding: "8px", borderBottom: "1px solid #eee" }}>
                {item.mall_name}
              </td>

              <td style={{ padding: "8px", borderBottom: "1px solid #eee", textAlign: "right" }}>
                {item.currency} {item.price.toLocaleString()}
                {item.price === min && (
                  <span
                    style={{
                      marginLeft: "8px",
                      padding: "2px 6px",
                      borderRadius: "999px",
                      backgroundColor: "#fee2e2",
                      color: "#b91c1c",
                      fontSize: "11px",
                    }}
                  >
                    최저가
                  </span>
                )}
              </td>

              <td style={{ textAlign: "center", padding: "8px", borderBottom: "1px solid #eee" }}>
                {item.url ? (
                  <a href={item.url} target="_blank" rel="noreferrer" style={{ color: "#2563eb" }}>
                    바로가기
                  </a>
                ) : (
                  "-"
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PriceTable;
EOF



################################
# ErrorMessage.js
################################
cat << 'EOF' > "$BASE_DIR/components/ErrorMessage.js"
import React from "react";

const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div
      style={{
        marginTop: "8px",
        marginBottom: "16px",
        padding: "10px 12px",
        borderRadius: "8px",
        backgroundColor: "#fef2f2",
        color: "#b91c1c",
        fontSize: "14px",
      }}
    >
      {message}
    </div>
  );
};

export default ErrorMessage;
EOF

echo "✅ 컴포넌트 생성 완료!"
read "ok?👉 다음 단계로 가려면 ENTER "



#######################################################
# STEP 4 — Pages 생성
#######################################################

echo ""
echo "====================================================="
echo "📄 STEP 4) Scanner 페이지 생성"
echo "====================================================="
sleep 1

cat << 'EOF' > "$BASE_DIR/pages/Scanner.js"
import React, { useState } from "react";
import SearchBar from "../components/SearchBar";
import ProductCard from "../components/ProductCard";
import PriceTable from "../components/PriceTable";
import ErrorMessage from "../components/ErrorMessage";
import { fetchProductByBarcode } from "../api/productApi";

const Scanner = () => {
  const [barcode, setBarcode] = useState("");
  const [product, setProduct] = useState(null);
  const [prices, setPrices] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setError("");
    setProduct(null);
    setPrices([]);
    setLoading(true);

    try {
      const data = await fetchProductByBarcode(barcode);

      if (data.product) setProduct(data.product);
      else setProduct(data);

      if (data.prices) setPrices(data.prices);
    } catch (err) {
      setError(err.message || "조회에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        padding: "40px 24px",
        maxWidth: "800px",
        margin: "0 auto",
      }}
    >
      <h1 style={{ fontSize: "32px", marginBottom: "24px" }}>
        Latam Beauty Scanner
      </h1>

      <SearchBar
        value={barcode}
        onChange={(e) => setBarcode(e.target.value)}
        onSubmit={handleSearch}
      />

      {loading && <p>조회 중...</p>}
      <ErrorMessage message={error} />

      {product && (
        <>
          <ProductCard product={product} />
          <PriceTable prices={prices} />
        </>
      )}
    </div>
  );
};

export default Scanner;
EOF

echo "📄 Scanner.js 생성 완료!"
read "ok?👉 다음 단계로 가려면 ENTER "



#######################################################
# STEP 5 — App.js 업데이트
#######################################################

echo ""
echo "====================================================="
echo "📌 STEP 5) App.js 업데이트"
echo "====================================================="
sleep 1

cat << 'EOF' > "$BASE_DIR/App.js"
import React from "react";
import "./App.css";
import Scanner from "./pages/Scanner";

function App() {
  return <Scanner />;
}

export default App;
EOF

echo "✨ App.js 업데이트 완료!"
read "ok?👉 마지막 확인을 위해 ENTER "



#######################################################
# STEP 6 — 완료 메시지
#######################################################

echo ""
echo "====================================================="
echo "🎉 모든 단계 완료! 프론트 구조가 성공적으로 정리되었습니다."
echo "====================================================="
echo ""
echo "📁 생성된 구조:"
echo "  $BASE_DIR/api"
echo "  $BASE_DIR/components"
echo "  $BASE_DIR/pages"
echo "  $BASE_DIR/styles"
echo ""
echo "이제 프론트 실행:   cd ~/latambeauty-app/frontend && npm start"
echo ""