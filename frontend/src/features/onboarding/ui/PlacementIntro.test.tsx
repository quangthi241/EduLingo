import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { PlacementIntro } from "./PlacementIntro";

describe("PlacementIntro", () => {
  it("renders explanation and Begin placement CTA", async () => {
    const onBegin = vi.fn();
    render(<PlacementIntro onBegin={onBegin} />);
    expect(screen.getByText(/takes about 10 minutes/i)).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /begin placement/i }));
    expect(onBegin).toHaveBeenCalledOnce();
  });
});
