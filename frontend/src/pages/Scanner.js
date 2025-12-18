import React, { useState } from "react";
import { useNavigate } from "react-router-dom";  // ✅ Search 페이지 이동 위해 필요
import SearchBar from "../components/search/SearchBar";
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

  const navigate = useNavigate(); // ✅ Search 페이지 이동

  // --------------------------------------------------------
  // 바코드 검색 처리
  // --------------------------------------------------------
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

      {/* 🔎 바코드 입력 SearchBar */}
      <SearchBar
        value={barcode}
        onChange={(e) => setBarcode(e.target.value)}
        onSubmit={handleSearch}
      />

      {/* 🔥 Search 페이지 이동 버튼 */}
      <button
        onClick={() => navigate("/search")}
        style={{
          padding: "12px",
          width: "100%",
          marginTop: "12px",
          borderRadius: "8px",
          border: "1px solid #ccc",
          background: "#fff",
          fontSize: "16px",
          cursor: "pointer",
        }}
      >
        🔍 제품명으로 검색하기
      </button>

      {/* 조회 중 표시 */}
      {loading && <p>조회 중...</p>}

      {/* 에러 메시지 */}
      <ErrorMessage message={error} />

      {/* 제품 정보 표시 */}
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