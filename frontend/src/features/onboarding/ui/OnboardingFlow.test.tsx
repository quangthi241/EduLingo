import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { OnboardingFlow } from "./OnboardingFlow";

const pushMock = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: pushMock }),
}));
vi.mock("@shared/api/client", () => ({
  apiFetch: vi.fn().mockResolvedValue({ id: "u1" }),
}));

describe("OnboardingFlow", () => {
  it("walks through goal → context → placement-intro", async () => {
    render(<OnboardingFlow />);
    await userEvent.click(screen.getByRole("button", { name: /IELTS/ }));
    expect(screen.getByText(/Your rhythm/)).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /continue/i }));
    expect(screen.getByText(/short placement/i)).toBeInTheDocument();
    await userEvent.click(screen.getByRole("button", { name: /begin placement/i }));
    expect(pushMock).toHaveBeenCalledWith("/placement-intro");
  });
});
