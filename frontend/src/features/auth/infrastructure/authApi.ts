import { apiFetch } from "@shared/api/client";
import type {
  AuthResponse,
  AuthUser,
  LoginPayload,
  RegisterPayload,
} from "../domain/types";

export const authApi = {
  register: (payload: RegisterPayload) =>
    apiFetch<AuthResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  login: (payload: LoginPayload) =>
    apiFetch<AuthResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  logout: () =>
    apiFetch<void>("/api/auth/logout", {
      method: "POST",
    }),
  me: () => apiFetch<AuthUser>("/api/auth/me"),
};
