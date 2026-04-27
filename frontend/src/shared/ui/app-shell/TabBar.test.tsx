import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { TabBar } from "./TabBar";

vi.mock("next/navigation", () => ({ usePathname: () => "/today" }));

describe("TabBar", () => {
  it("renders all 4 destinations with Today active", () => {
    render(<TabBar />);
    expect(screen.getByRole("link", { name: /today/i })).toHaveAttribute(
      "aria-current",
      "page",
    );
    expect(screen.getByRole("link", { name: /library/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /review/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /progress/i })).toBeInTheDocument();
  });
});
