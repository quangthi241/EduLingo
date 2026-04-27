import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ItemRow } from "./ItemRow";

describe("ItemRow", () => {
  it("renders title, meta, and trailing children", () => {
    render(
      <ItemRow title="The slow erosion of coastlines" meta="8 min · B2">
        <span data-testid="trailing">Read</span>
      </ItemRow>,
    );
    expect(screen.getByText(/erosion of coastlines/)).toBeInTheDocument();
    expect(screen.getByText("8 min · B2")).toBeInTheDocument();
    expect(screen.getByTestId("trailing")).toBeInTheDocument();
  });
});
