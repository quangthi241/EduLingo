import { describe, expect, it, beforeAll, afterAll, afterEach } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { setupServer } from "msw/node";

import { libraryHandlers } from "@/mocks/handlers/library";
import { LibraryIndex } from "./LibraryIndex";

const server = setupServer(...libraryHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("LibraryIndex", () => {
  it("renders pieces from the API", async () => {
    const client = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    render(
      <QueryClientProvider client={client}>
        <LibraryIndex />
      </QueryClientProvider>,
    );
    await waitFor(() =>
      expect(screen.getByText("Coastlines")).toBeInTheDocument(),
    );
  });
});
