import { http, HttpResponse } from "msw";

type Piece = Record<string, unknown> & { id: string; slug: string; status: string };

const store = new Map<string, Piece>();

function seed() {
  if (store.size) return;
  const base: Piece = {
    id: "00000000-0000-0000-0000-000000000100",
    slug: "draft-example",
    title: "Draft Example",
    cefr: "B1",
    minutes: 5,
    kind: "reading",
    topic: "travel",
    status: "draft",
    source: "editorial",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    publishedAt: null,
    body: {
      kind: "reading",
      text: "x".repeat(200),
      mcq: [
        { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
        { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
        { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
      ],
      shortAnswer: { prompt: "p", gradingNotes: "n" },
    },
  };
  store.set(base.id, base);
}

export const adminContentHandlers = [
  http.get("http://localhost:8000/api/admin/content", () => {
    seed();
    return HttpResponse.json({
      items: Array.from(store.values()),
      nextCursor: null,
    });
  }),

  http.get("http://localhost:8000/api/admin/content/:id", ({ params }) => {
    const p = store.get(String(params.id));
    return p
      ? HttpResponse.json(p)
      : HttpResponse.json(
          { type: "about:blank", title: "Not Found" },
          { status: 404 },
        );
  }),

  http.post("http://localhost:8000/api/admin/content", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const id = crypto.randomUUID();
    const now = new Date().toISOString();
    const piece: Piece = {
      id,
      slug: String(body.slug),
      title: String(body.title),
      cefr: String(body.cefr),
      minutes: Number(body.minutes),
      kind: String(body.kind),
      topic: String(body.topic),
      status: "draft",
      source: "editorial",
      createdAt: now,
      updatedAt: now,
      publishedAt: null,
      body: body.body,
    };
    store.set(id, piece);
    return HttpResponse.json(piece, { status: 201 });
  }),

  http.patch("http://localhost:8000/api/admin/content/:id", async ({ params, request }) => {
    const p = store.get(String(params.id));
    if (!p) return HttpResponse.json(null, { status: 404 });
    const patch = (await request.json()) as Record<string, unknown>;
    Object.assign(p, patch);
    p.updatedAt = new Date().toISOString();
    return HttpResponse.json(p);
  }),

  http.post("http://localhost:8000/api/admin/content/:id/publish", ({ params }) => {
    const p = store.get(String(params.id));
    if (!p) return HttpResponse.json(null, { status: 404 });
    p.status = "published";
    p.publishedAt = new Date().toISOString();
    return HttpResponse.json(p);
  }),

  http.post("http://localhost:8000/api/admin/content/:id/archive", ({ params }) => {
    const p = store.get(String(params.id));
    if (!p) return HttpResponse.json(null, { status: 404 });
    p.status = "archived";
    return HttpResponse.json(p);
  }),

  http.delete("http://localhost:8000/api/admin/content/:id", ({ params }) => {
    store.delete(String(params.id));
    return new HttpResponse(null, { status: 204 });
  }),

  http.post("http://localhost:8000/api/admin/content/:id/media", async ({ params }) => {
    const p = store.get(String(params.id));
    if (!p) return HttpResponse.json(null, { status: 404 });
    const body = p.body as Record<string, unknown>;
    body.audioRef = {
      storageKey: `pieces/${p.id}/audio.mp3`,
      mimeType: "audio/mpeg",
      durationSeconds: 30,
    };
    body.audioUrl = `/media/pieces/${p.id}/audio.mp3`;
    return HttpResponse.json(p);
  }),

  http.post("http://localhost:8000/api/admin/content/generate", async ({ request }) => {
    const input = (await request.json()) as Record<string, unknown>;
    const id = crypto.randomUUID();
    const now = new Date().toISOString();
    const piece: Piece = {
      id,
      slug: `generated-${id.slice(0, 6)}`,
      title: "Generated Piece",
      cefr: String(input.cefr),
      minutes: 6,
      kind: String(input.kind),
      topic: String(input.topic),
      status: "draft",
      source: "llm_generated",
      createdAt: now,
      updatedAt: now,
      publishedAt: null,
      body: {
        kind: input.kind,
        text: "x".repeat(300),
        mcq: [
          { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
          { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
          { question: "Q", choices: ["a", "b"], correctIndex: 0, rationale: "r" },
        ],
        shortAnswer: { prompt: "p", gradingNotes: "n" },
      },
    };
    store.set(id, piece);
    return HttpResponse.json(piece, { status: 201 });
  }),
];
