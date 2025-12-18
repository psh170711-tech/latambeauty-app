import axios from "./axiosConfig";

export const getProductByBarcode = (barcode) =>
  axios.get(`/products/barcode/${barcode}`);