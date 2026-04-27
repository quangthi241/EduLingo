import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Masthead } from "./Masthead";

describe("Masthead", () => {
  it("renders formatted date and goal badge", () => {
    render(
      <Masthead date={new Date("2026-04-21T09:00:00Z")} goalLabel="IELTS 7.0" />,
    );
    expect(screen.getByText(/Tuesday/i)).toBeInTheDocument();
    expect(screen.getByText("IELTS 7.0")).toBeInTheDocument();
  });
});
