import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { useState } from "react";

import { MCQBuilder } from "../ui/MCQBuilder";
import type { MCQ } from "@/features/library/domain/pieces";

function Harness({ onReady }: { onReady?: (val: MCQ[]) => void }) {
  const [val, setVal] = useState<MCQ[]>([
    { question: "Q1", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
    { question: "Q2", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
    { question: "Q3", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
  ]);
  return (
    <MCQBuilder
      value={val}
      onChange={(v) => {
        setVal(v);
        onReady?.(v);
      }}
    />
  );
}

describe("MCQBuilder", () => {
  it("adds a row", () => {
    const spy = vi.fn();
    render(<Harness onReady={spy} />);
    fireEvent.click(screen.getByRole("button", { name: /add question/i }));
    expect(spy).toHaveBeenCalled();
    expect(spy.mock.calls[0][0]).toHaveLength(4);
  });

  it("refuses to remove below 3", () => {
    render(<Harness />);
    const removes = screen.getAllByRole("button", { name: /remove/i });
    fireEvent.click(removes[0]);
    fireEvent.click(removes[1]);
    // Still 3 rows minimum
    expect(screen.getAllByLabelText(/Question \d/).length).toBe(3);
  });
});
