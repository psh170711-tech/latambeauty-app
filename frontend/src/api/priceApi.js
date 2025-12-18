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
