import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { ContextualRail } from "./ContextualRail";

vi.mock("next/navigation", () => ({ usePathname: () => "/library" }));

describe("ContextualRail", () => {
  it("renders Library sub-sections when route is /library", () => {
    render(<ContextualRail />);
    expect(screen.getByText("Reading")).toBeInTheDocument();
    expect(screen.getByText("Listening")).toBeInTheDocument();
    expect(screen.getByText("Speaking")).toBeInTheDocument();
    expect(screen.getByText("Writing")).toBeInTheDocument();
  });
});
