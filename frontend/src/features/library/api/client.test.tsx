import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import { setupServer } from "msw/node";
import type { ReactNode } from "react";

import { libraryHandlers } from "@/mocks/handlers/library";
import { useLibraryPieceQuery, useLibraryQuery } from "./client";

const server = setupServer(...libraryHandlers);

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

describe("useLibraryQuery", () => {
  it("fetches the library index", async () => {
    const { result } = renderHook(() => useLibraryQuery({ cefr: "B1" }), {
      wrapper,
    });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.items[0].slug).toBe("coastlines");
  });
});

describe("useLibraryPieceQuery", () => {
  it("fetches a single piece by slug", async () => {
    const { result } = renderHook(() => useLibraryPieceQuery("coastlines"), {
      wrapper,
    });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data?.slug).toBe("coastlines");
  });
});
