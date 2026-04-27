import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { setupServer } from "msw/node";
import type { ReactNode } from "react";

import { adminContentHandlers } from "@/mocks/handlers/admin-content";
import { useAdminPiecesQuery } from "./client";

const server = setupServer(...adminContentHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function wrapper({ children }: { children: ReactNode }) {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return (
    <QueryClientProvider client={client}>{children}</QueryClientProvider>
  );
}

describe("useAdminPiecesQuery", () => {
  it("fetches admin pieces", async () => {
    const { result } = renderHook(() => useAdminPiecesQuery(), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.items.length).toBeGreaterThanOrEqual(1);
  });
});
