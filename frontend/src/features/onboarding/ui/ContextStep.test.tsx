import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { ContextStep } from "./ContextStep";

describe("ContextStep", () => {
  it("submits selected minutes and starting hint", async () => {
    const onNext = vi.fn();
    render(<ContextStep suggestedMinutes={20} onNext={onNext} />);
    await userEvent.click(screen.getByRole("radio", { name: /30/ }));
    await userEvent.click(screen.getByRole("radio", { name: /intermediate/i }));
    await userEvent.click(screen.getByRole("button", { name: /continue/i }));
    expect(onNext).toHaveBeenCalledWith({ minutesPerDay: 30, startingHint: "intermediate" });
  });
});
