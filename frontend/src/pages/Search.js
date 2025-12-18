import React, { useState } from "react";
import SearchBar from "../components/search/SearchBar";
import ProductCard from "../components/ProductCard";
import PriceTable from "../components/PriceTable";
import ErrorMessage from "../components/ErrorMessage";
import { searchProducts } from "../api/productApi";

// 🔎 제품 검색 페이지
const Search = () => {
  const [keyword, setKeyword] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  // 🔍 검색 실행
  const handleSearch = async () => {
    if (!keyword.trim()) {
      setError("검색어를 입력해주세요.");
      return;
    }

    try {
      setError("");
      const data = await searchProducts(keyword);

      if (!data || data.length === 0) {
        setError("검색 결과가 없습니다.");
        setResults([]);
        return;
      }

      setResults(data);
    } catch (err) {
      setError(err.message || "검색 중 오류가 발생했습니다.");
    }
  };

  return (
    <div style={{ padding: "24px", maxWidth: "800px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "16px" }}>제품 검색</h1>

      {/* 검색바 */}
      <SearchBar
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        onSubmit={handleSearch}
      />

      {/* 에러 메시지 */}
      <ErrorMessage message={error} />

      {/* 검색 결과 출력 */}
      {results.map((product) => (
        <div key={product.id} style={{ marginBottom: "24px" }}>
          <ProductCard product={product} />
          <PriceTable prices={product.offers || []} />
        </div>
      ))}
    </div>
  );
};

export default Search;