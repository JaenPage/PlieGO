import axios from "axios";

function computeBaseURL(): string {
  // 1) Si hay env, úsalo
  const env = import.meta.env.VITE_API_URL as string | undefined;
  if (env) return env.replace(/\/+$/, "");

  // 2) Fallback: mismo host del navegador, puerto 8000
  const { protocol, hostname } = window.location;
  const base = `${protocol}//${hostname}:8000/api/v1`;
  return base;
}

export const api = axios.create({
  baseURL: computeBaseURL(),
  timeout: 60000,
});
