import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { Field, Label, Input, FieldError } from "./Field";

describe("Field", () => {
  it("associates label with input via htmlFor", () => {
    render(
      <Field>
        <Label htmlFor="email">Email</Label>
        <Input id="email" name="email" />
      </Field>,
    );
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
  });

  it("renders error with role=alert", () => {
    render(<FieldError>Required</FieldError>);
    expect(screen.getByRole("alert")).toHaveTextContent("Required");
  });
});
