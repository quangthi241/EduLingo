import { http, HttpResponse } from "msw";

const MOCK_PIECES = [
  {
    id: "00000000-0000-0000-0000-000000000001",
    slug: "coastlines",
    title: "Coastlines",
    cefr: "B1",
    minutes: 6,
    kind: "reading",
    topic: "travel",
    status: "published",
    source: "editorial",
    createdAt: "2026-04-20T00:00:00Z",
    updatedAt: "2026-04-20T00:00:00Z",
    publishedAt: "2026-04-20T00:00:00Z",
    body: {
      kind: "reading",
      text: "Northern Portuguese coast ...".repeat(10),
      mcq: [
        {
          question: "Q1",
          choices: ["a", "b", "c"],
          correctIndex: 0,
          rationale: "r",
        },
        {
          question: "Q2",
          choices: ["a", "b"],
          correctIndex: 1,
          rationale: "r",
        },
        {
          question: "Q3",
          choices: ["a", "b", "c"],
          correctIndex: 2,
          rationale: "r",
        },
      ],
      shortAnswer: { prompt: "Summarize", gradingNotes: "n" },
    },
  },
];

export const libraryHandlers = [
  http.get("http://localhost:8000/api/library", () =>
    HttpResponse.json({ items: MOCK_PIECES, nextCursor: null }),
  ),

  http.get("http://localhost:8000/api/library/:slug", ({ params }) => {
    const found = MOCK_PIECES.find((p) => p.slug === params.slug);
    return found
      ? HttpResponse.json(found)
      : HttpResponse.json(
          { type: "about:blank", title: "Not Found" },
          { status: 404 },
        );
  }),
];
