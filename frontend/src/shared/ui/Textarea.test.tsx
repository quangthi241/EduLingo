import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { Textarea } from "./Textarea";

describe("Textarea", () => {
  it("renders label and value", () => {
    render(<Textarea label="Notes" id="notes" defaultValue="hello" />);
    expect(screen.getByLabelText("Notes")).toHaveValue("hello");
  });

  it("announces error via aria-describedby", () => {
    render(<Textarea label="Notes" id="notes" error="required" />);
    const el = screen.getByLabelText("Notes");
    expect(el).toHaveAttribute("aria-describedby", "notes-error");
    expect(screen.getByText("required")).toHaveAttribute("id", "notes-error");
  });
});
