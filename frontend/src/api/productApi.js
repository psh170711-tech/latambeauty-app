import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

// -------------------------------------------------
// 1) 바코드 → 제품 조회 (Scanner용)
// -------------------------------------------------
export async function fetchProductByBarcode(barcode) {
  if (!barcode || !barcode.trim()) {
    throw new Error("바코드를 입력해주세요.");
  }

  try {
    const response = await axios.get(
      `${API_BASE_URL}/products/barcode/${encodeURIComponent(
        barcode.trim()
      )}`
    );
    return response.data;
  } catch (error) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error("제품 조회 중 오류가 발생했습니다.");
  }
}

// -------------------------------------------------
// 2) 제품 검색 (Search 페이지용)
//    /products/search?keyword=XXX
// -------------------------------------------------
export async function searchProducts(keyword) {
  if (!keyword || keyword.trim() === "") {
    throw new Error("검색어를 입력해주세요.");
  }

  try {
    const response = await axios.get(`${API_BASE_URL}/products/search`, {
      params: { keyword },
    });
    return response.data;
  } catch (error) {
    throw new Error("검색 중 오류가 발생했습니다.");
  }
}

// -------------------------------------------------
// 3) ID로 제품 상세 조회 (ProductDetail)
// -------------------------------------------------
export async function fetchProductById(id) {
  try {
    const response = await axios.get(`${API_BASE_URL}/products/${id}`);
    return response.data;
  } catch (error) {
    throw new Error("제품 상세 정보를 불러오는 중 오류가 발생했습니다.");
  }
}