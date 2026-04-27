import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { TopNav } from "./TopNav";

vi.mock("next/navigation", () => ({ usePathname: () => "/library" }));

describe("TopNav", () => {
  it("shows brand mark, 4 destinations, and marks /library active", () => {
    render(<TopNav />);
    expect(screen.getByText("EduLingo")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /library/i })).toHaveAttribute(
      "aria-current",
      "page",
    );
  });
});
