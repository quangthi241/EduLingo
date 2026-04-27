import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { PiecePage } from "./PiecePage";
import type { Piece } from "../domain/pieces";

const readingPiece: Piece = {
  id: "x",
  slug: "coastlines",
  title: "Coastlines",
  cefr: "B2",
  minutes: 8,
  kind: "reading",
  topic: "travel",
  status: "published",
  source: "editorial",
  createdAt: "2026-04-20T00:00:00Z",
  updatedAt: "2026-04-20T00:00:00Z",
  publishedAt: "2026-04-20T00:00:00Z",
  body: {
    kind: "reading",
    text: "Once upon a shore…",
    mcq: [],
    shortAnswer: { prompt: "p", gradingNotes: "n" },
  },
};

const listeningPiece: Piece = {
  id: "y",
  slug: "night-radio",
  title: "Night Radio",
  cefr: "B1",
  minutes: 5,
  kind: "listening",
  topic: "culture",
  status: "published",
  source: "editorial",
  createdAt: "2026-04-20T00:00:00Z",
  updatedAt: "2026-04-20T00:00:00Z",
  publishedAt: "2026-04-20T00:00:00Z",
  body: {
    kind: "listening",
    audioRef: {
      storageKey: "seeds/night-radio/night-radio.mp3",
      mimeType: "audio/mpeg",
      durationSeconds: 30,
    },
    audioUrl: "/media/seeds/night-radio/night-radio.mp3",
    transcript: "You're listening to Midnight FM.",
    mcq: [],
    shortAnswer: { prompt: "p", gradingNotes: "n" },
  },
};

describe("PiecePage", () => {
  it("renders piece title and Start-as-exercise CTA", () => {
    render(<PiecePage piece={readingPiece} />);
    expect(screen.getByRole("heading", { name: /coastlines/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /start as exercise/i })).toHaveAttribute(
      "href",
      "/session/library-coastlines",
    );
  });
});

describe("PiecePage listening variant", () => {
  it("renders audio when audioUrl present", () => {
    render(<PiecePage piece={listeningPiece} />);
    expect(screen.getByLabelText("Night Radio audio")).toHaveAttribute(
      "src",
      "/media/seeds/night-radio/night-radio.mp3",
    );
  });
});
