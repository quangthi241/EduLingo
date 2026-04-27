import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ProfilePage from "./page";

describe("ProfilePage", () => {
  it("renders profile sections (appearance, account)", () => {
    render(<ProfilePage />);
    expect(screen.getByRole("heading", { name: /profile/i })).toBeInTheDocument();
    expect(screen.getByText(/appearance/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign out/i })).toBeInTheDocument();
  });
});
