import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Section, Card } from "./Card";

describe("Section / Card", () => {
  it("Section renders heading with eyebrow", () => {
    render(
      <Section eyebrow="Intake" heading="Today's reading">
        <p>body</p>
      </Section>,
    );
    expect(screen.getByText("Intake")).toBeInTheDocument();
    expect(
      screen.getByRole("heading", { name: "Today's reading" }),
    ).toBeInTheDocument();
  });

  it("Card renders children", () => {
    render(<Card>hello</Card>);
    expect(screen.getByText("hello")).toBeInTheDocument();
  });
});
