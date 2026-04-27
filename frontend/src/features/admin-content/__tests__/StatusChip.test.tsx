import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusChip } from "../ui/StatusChip";

describe("StatusChip", () => {
  it("renders a Draft chip", () => {
    render(<StatusChip status="draft" />);
    expect(screen.getByText("Draft")).toBeInTheDocument();
  });
  it("renders a Published chip", () => {
    render(<StatusChip status="published" />);
    expect(screen.getByText("Published")).toBeInTheDocument();
  });
});
