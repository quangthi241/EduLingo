import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { Button } from "./Button";

describe("Button", () => {
  it("renders children and fires onClick", async () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Start placement</Button>);
    await userEvent.click(screen.getByRole("button", { name: /start placement/i }));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it("applies ghost variant styles", () => {
    render(<Button variant="ghost">Back</Button>);
    const btn = screen.getByRole("button");
    expect(btn).toHaveAttribute("data-variant", "ghost");
  });

  it("disables when loading", () => {
    render(<Button loading>Save</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
