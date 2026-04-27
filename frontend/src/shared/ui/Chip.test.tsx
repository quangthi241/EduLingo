import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { Chip } from "./Chip";

describe("Chip", () => {
  it("renders label", () => {
    render(<Chip tone="info">Draft</Chip>);
    expect(screen.getByText("Draft")).toBeInTheDocument();
  });

  it("applies tone class", () => {
    const { container } = render(<Chip tone="success">Published</Chip>);
    expect(container.firstChild).toHaveClass(/success|green/);
  });
});
