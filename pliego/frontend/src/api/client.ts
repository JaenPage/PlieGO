import axios from "axios";

// Usamos proxy de Vite: todas las llamadas empiezan por /api
export const api = axios.create({
  baseURL: "/api/v1",
  timeout: 60000,
});
