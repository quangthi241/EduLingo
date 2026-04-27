import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { TodayBrief } from "./TodayBrief";

const MOCK = {
  date: new Date("2026-04-21T09:00:00Z"),
  goalLabel: "IELTS 7.0",
  intake: { title: "The slow erosion of coastlines", minutes: 8, cefr: "B2" },
  practice: { grammar: "Past perfect after 'by the time'", vocab: ["erode", "sediment", "mitigation"] },
  produce: { prompt: "Summarise the main argument in 4 sentences." },
  reflection: "What was the writer's strongest claim?",
};

describe("TodayBrief", () => {
  it("renders all four sections + reflection", () => {
    render(<TodayBrief data={MOCK} />);
    expect(screen.getByText(/Tuesday/)).toBeInTheDocument();
    expect(screen.getByText("IELTS 7.0")).toBeInTheDocument();
    expect(screen.getByText(/coastlines/)).toBeInTheDocument();
    expect(screen.getByText(/Past perfect/)).toBeInTheDocument();
    expect(screen.getByText(/Summarise the main argument/)).toBeInTheDocument();
    expect(screen.getByText(/strongest claim/)).toBeInTheDocument();
  });
});
