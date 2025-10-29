import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const registerUser = (data) => API.post("/users/register", data);
export const loginUser = (data) => API.post("/users/login", data);
export const getAccounts = (token) =>
  API.get("/accounts/", { headers: { Authorization: `Bearer ${token}` } });
export const getTransactions = (accountId, token) =>
  API.get(`/transactions/${accountId}`, { headers: { Authorization: `Bearer ${token}` } });
export const transfer = (data, token) =>
  API.post("/transactions/transfer", data, { headers: { Authorization: `Bearer ${token}` } });