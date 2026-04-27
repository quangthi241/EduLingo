import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import MarketingPage from "./page";

describe("MarketingPage", () => {
  it("renders editorial hero and placement CTA", () => {
    render(<MarketingPage />);
    expect(
      screen.getByRole("heading", { level: 1, name: /private.*coach/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /start placement/i })).toHaveAttribute(
      "href",
      "/login",
    );
    expect(screen.getByText(/listening/i)).toBeInTheDocument();
    expect(screen.getByText(/reading/i)).toBeInTheDocument();
    expect(screen.getByText(/speaking/i)).toBeInTheDocument();
    expect(screen.getByText(/writing/i)).toBeInTheDocument();
  });
});
