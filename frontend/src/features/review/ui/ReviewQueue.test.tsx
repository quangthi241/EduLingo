import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ReviewQueue } from "./ReviewQueue";

describe("ReviewQueue", () => {
  it("renders due count and grammar + vocabulary rows", () => {
    render(<ReviewQueue />);
    expect(screen.getByText(/due today/i)).toBeInTheDocument();
    expect(screen.getByText(/grammar/i)).toBeInTheDocument();
    expect(screen.getByText(/vocabulary/i)).toBeInTheDocument();
  });
});
