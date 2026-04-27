import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AppShell } from "./AppShell";

vi.mock("next/navigation", () => ({ usePathname: () => "/today" }));

describe("AppShell", () => {
  it("renders TopNav, TabBar, skip link, and children", () => {
    render(
      <AppShell>
        <p>page content</p>
      </AppShell>,
    );
    expect(screen.getByText("EduLingo")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /skip to content/i })).toHaveAttribute(
      "href",
      "#main",
    );
    expect(screen.getByText("page content")).toBeInTheDocument();
  });
});
