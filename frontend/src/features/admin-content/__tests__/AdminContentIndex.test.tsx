import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { setupServer } from "msw/node";

import { adminContentHandlers } from "@/mocks/handlers/admin-content";
import { AdminContentIndex } from "../ui/AdminContentIndex";

const server = setupServer(...adminContentHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("AdminContentIndex", () => {
  it("renders admin pieces from MSW", async () => {
    const client = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    render(
      <QueryClientProvider client={client}>
        <AdminContentIndex />
      </QueryClientProvider>,
    );
    await waitFor(() =>
      expect(screen.getByText("Draft Example")).toBeInTheDocument(),
    );
  });
});
