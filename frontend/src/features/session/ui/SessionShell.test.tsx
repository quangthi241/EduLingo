import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import { SessionShell } from "./SessionShell";

describe("SessionShell", () => {
  it("steps through Intake → Practice → Produce", async () => {
    render(<SessionShell sessionId="today-intake" />);
    expect(screen.getByText(/intake/i)).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /next/i }));
    expect(screen.getByText(/practice/i)).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /next/i }));
    expect(screen.getByText(/produce/i)).toBeInTheDocument();
  });
});
