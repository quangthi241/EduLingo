import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { Select } from "./Select";

describe("Select", () => {
  it("renders options", () => {
    render(
      <Select
        label="Kind"
        id="kind"
        options={[
          { value: "reading", label: "Reading" },
          { value: "listening", label: "Listening" },
        ]}
      />,
    );
    expect(screen.getByLabelText("Kind")).toBeInTheDocument();
    expect(screen.getByRole("option", { name: "Reading" })).toBeInTheDocument();
  });
});
