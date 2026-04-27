import { describe, it, expect } from "vitest";
import { GOAL_PRESETS, getPreset } from "./presets";

describe("GOAL_PRESETS", () => {
  it("lists five presets", () => {
    expect(GOAL_PRESETS.map((p) => p.id)).toEqual([
      "ielts", "toefl", "fluency", "professional", "travel",
    ]);
  });

  it("getPreset returns the matching preset or undefined", () => {
    expect(getPreset("ielts")?.label).toBe("IELTS");
    expect(getPreset("nope")).toBeUndefined();
  });
});
