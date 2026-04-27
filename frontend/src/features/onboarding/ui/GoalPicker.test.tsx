import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { GoalPicker } from "./GoalPicker";

describe("GoalPicker", () => {
  it("renders all 5 presets and calls onSelect with the chosen id", async () => {
    const onSelect = vi.fn();
    render(<GoalPicker onSelect={onSelect} />);
    expect(screen.getByText("IELTS")).toBeInTheDocument();
    expect(screen.getByText("TOEFL")).toBeInTheDocument();
    expect(screen.getByText("Travel")).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /IELTS/ }));
    expect(onSelect).toHaveBeenCalledWith("ielts");
  });
});
