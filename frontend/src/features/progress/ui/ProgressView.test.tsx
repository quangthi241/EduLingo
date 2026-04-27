import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { ProgressView } from "./ProgressView";

describe("ProgressView", () => {
  it("renders adaptive hero, days-on-pathway, and 6 skill meters", () => {
    render(<ProgressView />);
    expect(screen.getByText(/days on pathway/i)).toBeInTheDocument();
    expect(screen.queryByText(/streak/i)).toBeNull();
    ["Listening", "Reading", "Speaking", "Writing", "Grammar", "Vocabulary"].forEach(
      (s) => expect(screen.getByText(s)).toBeInTheDocument(),
    );
  });
});
