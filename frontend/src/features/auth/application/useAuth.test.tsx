import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";
import type { ReactNode } from "react";
import { useLogin } from "./useAuth";

const server = setupServer(
  http.post("http://localhost:8000/api/auth/login", async ({ request }) => {
    const body = (await request.json()) as { email: string; password: string };
    if (body.password === "correct") {
      return HttpResponse.json({
        userId: "11111111-1111-1111-1111-111111111111",
        email: body.email,
        role: "learner",
      });
    }
    return HttpResponse.json(
      { title: "not_found", detail: "invalid credentials", status: 404 },
      { status: 404, headers: { "Content-Type": "application/problem+json" } },
    );
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function wrapper({ children }: { children: ReactNode }) {
  const qc = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return <QueryClientProvider client={qc}>{children}</QueryClientProvider>;
}

describe("useLogin", () => {
  it("returns the auth response on success", async () => {
    const { result } = renderHook(() => useLogin(), { wrapper });

    result.current.mutate({ email: "a@b.co", password: "correct" });

    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toEqual({
      userId: "11111111-1111-1111-1111-111111111111",
      email: "a@b.co",
      role: "learner",
    });
  });

  it("surfaces ApiError on wrong password", async () => {
    const { result } = renderHook(() => useLogin(), { wrapper });

    result.current.mutate({ email: "a@b.co", password: "wrong" });

    await waitFor(() => expect(result.current.isError).toBe(true));
    expect((result.current.error as Error).message).toContain("invalid credentials");
  });
});
