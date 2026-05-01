import { ApiError } from "./errors";

const DEFAULT_BASE_URL = "http://localhost:8000";
const DEFAULT_INTERNAL_BASE_URL = "http://backend:8000";

export function apiBaseUrl(): string {
  // On the server (SSR / RSC), prefer the internal Docker network URL.
  if (typeof window === "undefined") {
    return process.env.INTERNAL_API_BASE_URL ?? DEFAULT_INTERNAL_BASE_URL;
  }
  return process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_BASE_URL;
}

export async function apiFetch<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const isFormData = init.body instanceof FormData;
  const res = await fetch(`${apiBaseUrl()}${path}`, {
    ...init,
    credentials: "include",
    headers: {
      ...(isFormData ? {} : { "Content-Type": "application/json" }),
      ...(init.headers ?? {}),
    },
  });
  if (!res.ok) {
    const body = (await res.json().catch(() => ({}))) as {
      title?: string;
      detail?: string;
    };
    throw new ApiError(
      body.title ?? "error",
      body.detail ?? res.statusText,
      res.status,
    );
  }
  if (res.status === 204) {
    return undefined as T;
  }
  return (await res.json()) as T;
}
