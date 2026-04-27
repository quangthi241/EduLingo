import { describe, expect, it, beforeAll, afterAll, afterEach, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { setupServer } from "msw/node";

import { adminContentHandlers } from "@/mocks/handlers/admin-content";
import { GenerateWizard } from "../ui/GenerateWizard";

const pushMock = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}));

const server = setupServer(...adminContentHandlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe("GenerateWizard", () => {
  it("generates a preview and allows saving", async () => {
    const client = new QueryClient({
      defaultOptions: { mutations: { retry: false }, queries: { retry: false } },
    });
    render(
      <QueryClientProvider client={client}>
        <GenerateWizard />
      </QueryClientProvider>,
    );

    fireEvent.click(screen.getByRole("button", { name: /generate/i }));

    await waitFor(() =>
      expect(screen.getByText(/Generated Piece/i)).toBeInTheDocument(),
    );

    expect(
      screen.getByRole("button", { name: /save as draft/i }),
    ).toBeInTheDocument();
  });
});
