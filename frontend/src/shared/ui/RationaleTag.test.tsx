import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { RationaleTag } from "./RationaleTag";

describe("RationaleTag", () => {
  it("renders label and reason with prefix", () => {
    render(<RationaleTag label="Grammar" reason="recurring past-perfect slips" />);
    expect(screen.getByText("Grammar")).toBeInTheDocument();
    expect(screen.getByText(/because.*past-perfect/i)).toBeInTheDocument();
  });
});
